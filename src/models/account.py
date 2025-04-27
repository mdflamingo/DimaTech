from pydantic import BaseModel


class Account(BaseModel):
    balance: float
