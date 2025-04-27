import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from werkzeug.security import check_password_hash, generate_password_hash

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(50), nullable=False)

    def __init__(self, email: str, password: str, full_name: str) -> None:
        self.email = email
        self.password = generate_password_hash(password)
        self.full_name = full_name

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f"<User {self.email}>"


class Admin(Base):
    __tablename__ = "admin"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(50), nullable=False)

    def __init__(self, email: str, password: str, full_name: str) -> None:
        self.email = email
        self.password = generate_password_hash(password)
        self.full_name = full_name

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f"<User {self.email}>"
