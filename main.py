from spider.Spider import TcgSpider
from staging.gsheets_agent import GoogleSheets
import json 
import os
GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_CREDENTIALS")
GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID")
from dotenv import load_dotenv

load_dotenv(".env")

spider = TcgSpider(use_default_query = True)
with open("keys.json","r") as jfile:
    GOOGLE_CREDENTIALS = dict(json.load(jfile))
print(GOOGLE_CREDENTIALS)

for i in range(200):
    page_data = spider.crawl(page = i+1,stop_condition= 3)
    print(page_data)

    google_sheets = GoogleSheets(
        credentials_file = GOOGLE_CREDENTIALS,
        sheet_key=GOOGLE_SHEET_ID["GOOGLE_SHEET_ID"],
        worksheet_name='prices')

    break

    # google_sheets.write_header_if_doesnt_exist(
    #     ["Program", "Course", "Study_Center", "Name", "Registration_ID", "Email", "Complaint"])
    # google_sheets.append_rows([["Electrical Engineering",
    #                             "Power Electronics",
    #                             "Accra",
    #                             "Michael Kofi Armah",
    #                             "123456789",
    #                             "user@example.com",
    #                             "i need my modules"]])