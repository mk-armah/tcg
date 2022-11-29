import datetime
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


class ChromeSettings:
    def __init__(self,set_chrome_options = True, verbose: bool = False):
         
        self.verbose = verbose
        self.set_chrome_options = set_chrome_options


    def _set_chrome_options(self) -> None:
        """Sets chrome options for Selenium.
        Chrome options for headless browser is enabled.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        return chrome_options


    def chef(self,url: str, driver=None, verbose: bool = False):
        """
        Establishes connection with hyperlinks and return soup object

        Args:
            
            url:str | url to scrape
            driver:webdriver object | an already existing driver which has knowledge of a pre-assigned url
            verbose: Optional parameter to enhance verbosity

        Returns:
            
            soup:beautiful soup object
            driver:webdriver object
            
            """

        if driver is None:
            driver = webdriver.Chrome(options = self._set_chrome_options())    \
                        if self.set_chrome_options is True else  webdriver.Chrome()       #ChromeDriverManager().install()

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
            if self.verbose is not False:
                print(soup.prettify())
        
            return soup, driver