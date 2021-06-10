from pydantic import BaseModel
from decimal import Decimal


class productBase(BaseModel):
    product_code: str
    product_name: str
    price: Decimal
