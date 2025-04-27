from sqlalchemy import BigInteger, Column, String, ForeignKey, Float, Integer
from sqlalchemy.orm import declarative_base, relationship
from werkzeug.security import check_password_hash, generate_password_hash

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(50), nullable=False)

    accounts = relationship("Account", back_populates="user")

    def __init__(self, email: str, password: str, full_name: str) -> None:
        self.email = email
        self.password = generate_password_hash(password)
        self.full_name = full_name

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class Admin(Base):
    __tablename__ = "admins"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(50), nullable=False)


class Account(Base):
    __tablename__ = "accounts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    balance = Column(Float, default=0.0)
    user_id = Column(BigInteger, ForeignKey("users.id"))

    user = relationship("User", back_populates="accounts")
    payments = relationship("Payment", back_populates="account")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"))

    account = relationship("Account", back_populates="payments")


password = "your_password"
hashed_password = generate_password_hash(password)
print(hashed_password)
