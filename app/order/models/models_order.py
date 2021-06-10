from ext.base_class import BaseModel
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.types import Numeric
from datetime import datetime


class Order(BaseModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    product_code = Column(String)
    customer_fullname = Column(String)
    product_name = Column(String)
    total_amount = Column(Numeric(
        precision=8,
        scale=2,
        decimal_return_scale=2)
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
