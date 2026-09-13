from sqlalchemy import (Column,BigInteger,String,Text,Numeric,DateTime,ForeignKey,Integer)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.utils.db import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(BigInteger,primary_key=True,autoincrement=True)
    user_id = Column(BigInteger,ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    amount = Column(Numeric(10, 2),default=0,nullable=False)
    order_status = Column(String(20),default="pending",nullable=False)
    remarks = Column(Text,nullable=True)
    cancel_reason = Column(String(255),nullable=True)
    created_at = Column(DateTime,server_default=func.now(),nullable=False)
    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)

    # Relationships 
    

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(BigInteger,primary_key=True,autoincrement=True)
    product_id = Column(BigInteger,ForeignKey("products.id", ondelete="CASCADE"),nullable=False)
    product_variant_id = Column(Integer,ForeignKey("product_variants.id", ondelete="CASCADE"),nullable=True)
    order_id = Column(BigInteger,ForeignKey("orders.id", ondelete="CASCADE"),nullable=False)
    cart_id = Column(BigInteger,ForeignKey("carts.id", ondelete="SET NULL"),nullable=True)
    quantity = Column(Integer,default=1,nullable=False)
    rate = Column(Numeric(10, 2),default=0,nullable=False)
    created_at = Column(DateTime,server_default=func.now(),nullable=False)
    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)

    # Relationships


class Payment(Base):
    __tablename__ = "payments"

    id = Column(BigInteger,primary_key=True,autoincrement=True)
    user_id = Column(BigInteger,ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    order_id = Column(BigInteger,ForeignKey("orders.id", ondelete="CASCADE"),nullable=False)
    payment_method = Column(String(100),nullable=False)
    amount = Column(Numeric(10, 2),default=0,nullable=False)
    transaction_id = Column(String(100),nullable=True)
    payment_status = Column(String(20),default="pending",nullable=False)
    created_at = Column(DateTime,server_default=func.now(),nullable=False)
    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)

    # Relationships
