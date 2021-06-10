from pydantic import BaseModel, validator, ValidationError
from decimal import Decimal
from datetime import datetime


class orderModelBase(BaseModel):
    user_id: str
    product_code: str


    @validator('user_id')
    def user_id_alphanumeric(cls, v):
        validators = [" ", "", "True", "true", "False", "false"]
        if isinstance(v, str) and v not in validators:
            return v
        raise ValidationError("The value must be alphanumeric")


    @validator('product_code')
    def product_code_alphanumeric(cls, v):
        validators = [" ", "", "True", "true", "False", "false"]
        if isinstance(v, str) and v not in validators:
            return v
        raise ValidationError("The value must be alphanumeric")


class orderModelCreate(orderModelBase):
    customer_fullname: str
    product_name: str
    total_amount: Decimal


    class Config:
        orm_mode = True


class orderModelCreateResponse(orderModelCreate):
    id: int
    created_at: datetime


    class Config:
        orm_mode = True


class orderMessage(BaseModel):
    order_id: int
    customer_fullname: str
    product_name: str
    total_amount: Decimal
    created_at: datetime


class orderPayload(BaseModel):
    order: orderMessage


class orderModelBrokerMessage(BaseModel):
    producer: str
    sent_at: datetime
    type: str
    payload: orderPayload


class messageBaseResponse(orderMessage):
    queue_index: int


class orderModelUpdate(orderModelBase):
    ...


class orderModelUpdateResponse(orderModelBase):
    ...


class orderModelGetResponse(orderModelBase):
    ...


class orderModelListResponse(orderModelBase):
    ...
