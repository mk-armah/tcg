"""
data schema
"""

import datetime
from pydantic import BaseModel


class Schema(BaseModel):
    productname: str
    price: int | None
    product_seller: str | None
    market_price: int | None = None
    listed_median_price: int | None = None
    buylist_market_price: int|None = None
    image:str
    date: datetime.datetime|str = datetime.datetime.utcnow()
    ts:str


if __name__ == '__main__':

    print(Schema.__dict__)
