"""software test for spider"""

from .spider import *
import pandas as pd
from ..staging import gsheets_agent



def test_spider():

    spider = TcgSpider(use_default_query = True)
    
    data = spider.crawl(page=3)
    
    for i in data:
        print(i)
    

    

    dataframe = pd.DataFrame(worksheet.get_all_records())
    #test that number of NaN's in excel is tolerable