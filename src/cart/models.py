from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.utils.db import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(BigInteger,primary_key=True,autoincrement=True)
    user_id = Column(BigInteger,ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    product_id = Column(BigInteger,ForeignKey("products.id", ondelete="CASCADE"),nullable=False)
    product_variant_id = Column(Integer,ForeignKey("product_variants.id", ondelete="CASCADE"),nullable=True)
    quantity = Column(Integer,default=1,nullable=False)
    created_at = Column(DateTime,server_default=func.now(),nullable=False)
    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)

