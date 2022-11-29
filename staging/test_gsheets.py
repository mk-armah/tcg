"""Test script for staging"""
import pytest
from .gsheets_agent import *


@pytest.fixture
def test_google_sheet_connection():
    """test google sheet connection"""

    try:
        with open("keys.json","r") as jfile:
            GOOGLE_CREDENTIALS = dict(json.load(jfile))
    except Exception as exc:
        print("Unable to load json file")

    try:
        google_sheet = GoogleSheets(
            credentials_file = GOOGLE_CREDENTIALS,
            sheet_key=GOOGLE_CREDENTIALS['google_sheet_id'],
            worksheet_name='test')
    
    except KeyError as keyerror:
        print("{} was not found in dict".format(keyerror))
    
    except ValueError:
        print("check account_type in dict | value should be 'service_account'")

    else:
        print("connection to google sheets was successful")

    return google_sheet


def test_write_header_if_doesnt_exist(test_google_sheet_connection):
    """test function that writes headers/column names to the google sheets
    Args:
        test_gsheets|pytest fixture, a connection to google sheets
    Return:
    """
    
    google_sheet = test_google_sheet_connection
    columns=[
            'ProductName',
            'Price',
            'ProductSeller',
            'MarketPrice',
            'BuyListMarketPrice',
            'ListedMedianPrice',
            'Date',
            'Timestamp']

    #check if it writes headers if there is nothing
    try:
        test_worksheet = google_sheet.sheet_object #get worksheet object
        test_worksheet.clear() #clear all available entries
        all_values = test_worksheet.get_all_values()
        assert all_values ==  []
        print("Cleared testing worksheet")

    except AssertionError:
        print('Worksheet was not cleared')
    
    try:
        google_sheet.write_header_if_doesnt_exist(columns = columns) #write to header | this time, there shoudn't be any header
        headers = test_worksheet.row_values(1)
        assert columns == headers

    except AssertionError:
        print("Failed | Coudn't write to google sheet columns")


    #check if it doesn't write to header when there are headers already
    try:
        google_sheet.write_header_if_doesnt_exist(columns = columns) #write to header | this time, headers are available
        assert len(test_worksheet.get_all_values()) == 1

    except AssertionError:
        print("Test 2 of write_header_if_doesn't_exist Failed | Headers re-written to cell")


def test_append_rows(test_google_sheet_connection):

    google_sheet = test_google_sheet_connection
    
    try:
        google_sheet.append_rows([["Code Card - Silver Tempest Booster Pack - SWSH12: Silver Tempest (SWSH12)",
                                    "$0.25",
                                    "LisasLilCardStore",
                                    0.14,
                                    None,
                                    0.16,
                                    "2022-11-26 09:18:18.543640",
                                    1669454299]])
    except Exception as exc:
        print("Unable to load to excel")
                                							
    
if __name__ == '__main__':
    test_google_sheet_connection()
    test_write_header_if_doesnt_exist(test_google_sheet_connection)
    test_append_rows()