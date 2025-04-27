from pydantic import BaseModel


class AuthenticatedUser(BaseModel):
    email: str
    password: str
