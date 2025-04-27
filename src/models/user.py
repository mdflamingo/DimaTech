from re import I
from pydantic import BaseModel


class AuthenticatedUser(BaseModel):
    email: str
    password: str

class UserInDB(BaseModel):
    id: int
    full_name: str
    email: str
