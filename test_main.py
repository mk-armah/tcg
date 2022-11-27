import main
import pandas as pd


def test_main():
    try:
        google_sheet = main('test',200)
       
        worksheet = google_sheet.sheet_object

    except AssertionError:
        pass

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

        assertion = [True for i in non_null_columns if df[i].isna().any() is False else False]
        assert all(assertion) is True

    except AssertionError:
        print("Null values found in productname field")
