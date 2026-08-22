from sqlalchemy import Column, BigInteger, String, Text, DateTime
from sqlalchemy.sql import func

from src.utils.db import Base


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255),unique=True,nullable=False)
    slug = Column(String(255),unique=True,nullable=False)
    description = Column(Text,nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)