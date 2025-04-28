from pydantic import BaseModel


class Paymant(BaseModel):
    transaction_id: str
    user_id: int
    account_id: int
    amount: int
    signature: str
