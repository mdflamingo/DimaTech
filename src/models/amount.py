from pydantic import BaseModel


class Amount(BaseModel):
    amount: float
    account_id: int
