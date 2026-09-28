from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func

from src.utils.db import Base



class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    billing_address = Column(String(255), nullable=True)
    shipping_address = Column(String(255), nullable=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50),nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)


