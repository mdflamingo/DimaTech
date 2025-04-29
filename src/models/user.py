from pydantic import BaseModel

from models.account import Account


class UserInDB(BaseModel):
    id: int
    full_name: str
    email: str


class BaseUser(BaseModel):
    email: str
    password: str


class AuthenticatedUser(BaseUser): ...


class UserCreate(BaseUser):
    full_name: str


class UserUpdate(BaseUser):
    full_name: str


class UserList(UserInDB):
    accounts: list[Account]
