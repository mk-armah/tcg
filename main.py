import staging.schema as schema
from dotenv import dotenv_values
from spider_web.spider import TcgSpider
from staging.gsheets_agent import GoogleSheets
import json
import os
import datetime
GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_CREDENTIALS")
GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID")


credentials = dotenv_values(".env")

spider = TcgSpider(use_default_query=True)
with open("staging/keys.json", "r") as jfile:
    GOOGLE_CREDENTIALS = dict(json.load(jfile))


def main(worksheet,num_pages):
    """
        utilizes TCG-Spider to scrape data to google sheets

        Args:
            worksheet:str | name of worksheet to load
            num_pages:str | number of pages to scrape
    """

    google_sheets = GoogleSheets(
        credentials_file=GOOGLE_CREDENTIALS,
        sheet_key=GOOGLE_CREDENTIALS['google_sheet_id'],
        worksheet_name= worksheet)


    google_sheets.write_header_if_doesnt_exist(
        columns=[
            'ProductName',
            'Price',
            'ProductSeller',
            'MarketPrice',
            'BuyListMarketPrice',
            'ListedMedianPrice',
            'Date',
            'Timestamp'])


    for i in range(num_pages):
        page = spider.crawl(page=i + 1)
        for card in page:

            google_sheets.append_rows([list(card.values())])

        break
    return google_sheets


if __name__ == '__main__':
    main('prices',200)
