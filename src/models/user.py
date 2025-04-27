
from pydantic import BaseModel
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

