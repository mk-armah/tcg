"""
data schema
"""

import datetime
from pydantic import BaseModel



class Schema(BaseModel):
    productname: str
    price: int
    product_seller: str
    market_price: int | None = None
    listed_median_price: int | None = None
    buylist_market_price: int|None = None
    image:str
    date: datetime.datetime|str = datetime.datetime.utcnow()
    ts:str


if __name__ == '__main__':
    test_dict = {'productname': 'Michael',
                 'price': 20.0,
                 'product_seller': None}

    print(Schema.__dict__)
