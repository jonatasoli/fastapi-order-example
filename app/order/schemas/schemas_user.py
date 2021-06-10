from pydantic import BaseModel


class userBase(BaseModel):
    user_id: str
    firstName: str
    lastName: str
    customer_fullname: str
