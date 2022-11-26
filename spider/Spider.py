"""
Web Spider for tcgplayer.com.
This script was engineered from scratch
by,

Author : Ing. Michael Kofi Armah
Date:  17/11/22
copyright license attached
"""

import datetime
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class TcgSpider():

    def __init__(self, path: str = 'default', use_default_query=True, **query):

        self.host = 'https://www.tcgplayer.com'  # hostname
        self.path = path if path != 'default' else "/search/pokemon/product"  # path parameters

        # set query parameters
        if use_default_query:
            self.query = "?productLineName=pokemon&view=grid&ProductTypeName=Cards&page={}&CardType=Pokemon&inStock=true"
        else:
            self.query = "?productLineName={}&view={}&productTypeName={}&page={}&CardType={}&inStock={}"

            try:
                self.query = self.query.format(
                    query['productLineName'],
                    query['view'],
                    query['productTypeName'],
                    query['page'],
                    query['CardType'],
                    query['inStock'])
            except KeyError as keyerror:
                print("set parameter for : {}".format(keyerror))

        # url to scrape
        self.url = self.host + self.path + self.query

    def crawl(self, page, stop_condition: int | None = None):
        """
            Args:
                page:int | page to scrape .e.g 1, means scrape page 1
                stop_condition: int | an optionaly flag to stop iteration
                Stop condition is purposely developed to be used for test runs

            yields:
                page_data:list | list of all data found in a given page """

        print(self.url.format(page))

        soup, driver = self.Chef(url=self.url.format(page), driver=None)

        products = soup.find_all('div', {'class': 'search-result__content'})
        page_data = []
        data = {}
        # iterate over product grid
        for i, item_link in enumerate(products):

            card_url = self.host + item_link.find('a').get("href")

            print(card_url)
            try:
                driver.get(card_url)
                element = WebDriverWait(
                    driver, 20).until(
                    EC.visibility_of_all_elements_located(
                        (By.CLASS_NAME, "product-details__header")))

            except TimeoutException:
                print(
                    "Spider's connection was timeout while navigating through page {}".format(page))
            card_soup = BeautifulSoup(driver.page_source, 'html.parser')

            # get product name

            product_name_element = WebDriverWait(
                driver, 20).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "product-details__name")))

            product_name = product_name_element.get_attribute("innerHTML")
            data.update({"ProductName": product_name})

            # product_name = card_soup.find(
            #     'h1', {'class': 'product-details__name'})
            # data.update({"ProductName": product_name.text})

            # image
            # image_src = card_soup.find('img',{"class" : "v-lazy-image v-lazy-image-loaded"})
            # data.update({"image_src" : image_src['src']})
            # print(src)

            # get product price
            try:
                product_price_element = WebDriverWait(
                    driver, 20).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "spotlight__price")))

                assert product_name_element is not None
            except (AssertionError, TimeoutException):
                pass

            else:
                product_price = product_price_element.get_attribute(
                    "innerHTML")
                data.update({"Price": product_price})

            # product_price = card_soup.find(
            #     'span', {'class': 'spotlight__price'})
            # data.update({"Price": product_price.text})

            # product seller
            # seller's name is usually represented as "sold by
            # <cardseller's name>"
            try:
                product_seller_present = WebDriverWait(
                    driver, 20).until(
                    EC.text_to_be_present_in_element(
                        (By.CLASS_NAME, "spotlight__seller"), "Sold"))
                assert product_seller_present is True

            except (AssertionError, TimeoutException):
                print("Could not retrieve product seller name")
                data.update({"ProductSeller": None})
            else:
                product_seller = card_soup.find(
                    'section', {'class': 'spotlight__seller'}).text

                pattern = "by (.*)"
                try:
                    match = re.search(pattern, product_seller)
                    product_seller = match.group(1)
                    data.update({"ProductSeller": product_seller})
                    assert match is not None
                except AssertionError:
                    print("coudn't get card seller's name")  # log

            finally:
                pass

            # current price point
            current_price_points = card_soup.find(
                'ul', {'class': "price-points__rows"})
            current_price_points_tags = current_price_points.find_all('li')

            for li_tag in current_price_points_tags:
                cpp_data = str(li_tag.text)

                try:
                    assert cpp_data.__contains__("-") is not True
                    amount_isavailable = cpp_data.split("$")
                    # dictionary key | strip off all whitespaces
                    amount_label = amount_isavailable[0].strip().replace(
                        " ", "_").lower()
                    amount_value = amount_isavailable[1]  # dictionary value

                    # update with available true data
                    data.update({amount_label: amount_value})

                except AssertionError:

                    no_amount = cpp_data.split("-")
                    # update with null value represented as -
                    data.update(
                        {no_amount[0].strip().replace(" ", "_").lower(): None})

                finally:
                    continue

            current_time = datetime.datetime.utcnow()
            data.update({"Date": str(current_time)})
            data.update({"Ts": current_time.timestamp()})

            if i == stop_condition:
                break

            yield data

    def Chef(self, url: str, driver=None, verbose: bool = False):
        """
        establishes connection with hyperlinks and return soup object

        Args:
            url:str | url to scrape
            driver:webdriver object | an already existing driver which has knowledge of a pre-assigned url
            verbose: Optional parameter to enhance verbosity

        Returns:
            soup:beautiful soup object
            driver:webdriver object
            """

        if driver is None:
            driver = webdriver.Chrome(ChromeDriverManager().install())
            #driver = webdriver.Chrome()

        driver.get(url)

        try:
            WebDriverWait(
                driver, 20).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "search-results")))

        except TimeoutException as timeout:
            print(
                "Spider wasn't fast enough | Connection Timed Out - Error Code : 1001-prior | {}".format()),
        except Exception as exec:
            print("An error occured while scraping data {}".format(exec))

        finally:

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            if verbose is not False:
                print(soup.prettify())
            return soup, driver


if __name__ == "__main__":

    spider = TcgSpider(use_default_query=True)
    data = spider.crawl(page=1, stop_condition=3)
    for i in data:
        print(i)
