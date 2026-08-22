from sqlalchemy import Column, Integer, String, Text, DateTime,BigInteger,ForeignKey
from sqlalchemy.sql import func

from src.utils.db import Base


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(Integer,primary_key=True,autoincrement=True)
    product_id = Column(BigInteger,ForeignKey("products.id"),nullable=False)
    variant_name = Column(String(255),nullable=False)
    variant_type = Column(String(20),nullable=False)
    variant_value = Column(String(20),nullable=False)
    description = Column(Text,nullable=True)
    created_at = Column(DateTime,server_default=func.now(),nullable=False)
    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)