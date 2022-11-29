from main import main as bot
import pandas as pd


def test_main():
    try:
        google_sheet = bot('test',200)
       
        worksheet = google_sheet.sheet_object

    except AssertionError as assertionerror:
        raise assertionerror

    try:
        #test for nulls in columns

        df = pd.DataFrame(worksheet.get_all_records())
        
        # assert df['ProductName'].isna().any() == False
        # assert df['Price'].isna().any() == False
        # assert df['ProductSeller']

        non_null_columns = ['ProductName',
                            'Price',
                            'ProductSeller',
                            'MarketPrice',
                            'ListedMedianPrice',
                            'Date',
                            'Timestamp']

        assertion = [True if df[i].isna().any() is False else False for i in non_null_columns]
        assert all(assertion) is True

    except AssertionError:
        print("Null values found in productname field")


if __name__ == '__main__':
    test_main()

#tips on functionality testing
# test lenght of records ==25
# test datatypes of columns 
