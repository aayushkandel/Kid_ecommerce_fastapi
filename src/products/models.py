from sqlalchemy import Column, BigInteger, String, Text, DateTime,ForeignKey,Integer
from sqlalchemy.sql import func
from src.utils.db import Base
from sqlalchemy.orm import relationship

class Products(Base):
    __tablename__="products"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    category_id=Column(BigInteger,ForeignKey("categories.id"),nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    price=Column(Integer,nullable=False)
    stock_level=Column(Integer,nullable=True)
    created_at = Column(DateTime,server_default=func.now(),nullable=False)
    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False )
    

    category = relationship("Category", back_populates="products")
    product_rates = relationship("ProductRate",back_populates="products")



class ProductGallery(Base):
    __tablename__="product_gallery"

    id= Column(BigInteger,primary_key=True,autoincrement=True)
    product_id=Column(BigInteger,ForeignKey("products.id"),nullable=False)
    image=Column(String(500),nullable=False)

class ProductRate(Base):
    __tablename__ ="product_rates"
    id= Column(BigInteger,primary_key=True,autoincrement=True)
    rate=Column(Integer,nullable=False)
    stock_level=Column(Integer,nullable=False)
    product_id=Column(BigInteger,ForeignKey("products.id"),nullable=False)
    product_variant_id=Column(Integer,ForeignKey("product_variants.id"),nullable=True)
    created_at = Column(DateTime,server_default=func.now(),nullable=False)
    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)

    products=relationship("Products",back_populates="product_rates")
    product_variants=relationship("ProductVariant",back_populates="product_rates")
