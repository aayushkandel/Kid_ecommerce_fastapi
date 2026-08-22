from src.cart.dtos import cartBase,cartUpdateBase
from sqlalchemy.orm import Session
from src.cart.models import Cart
from fastapi import HTTPException,status
from src.user.models import User
from src.products.models import Products
from src.product_varients.models import ProductVariant

def create_cart(body:cartBase,db:Session,user:User):
    exist_product=db.query(Products).filter(Products.id==body.product_id).first()
    if not exist_product:
                raise HTTPException(status_code=404,detail=f"Product with given product id {body.product_id} doesnot exist")
    exist_user=db.query(User).filter(User.id==user.id).first()
    if not exist_user:
                raise HTTPException(status_code=404,detail=f"user with given user id {body.user_id} doesnot exist")
    if body.product_variant_id is not None:
       exist_product_variants=db.query(ProductVariant).filter(ProductVariant.id==body.product_variant_id).first() 
       if not exist_product_variants:
                   raise HTTPException(status_code=404,detail=f"Product_variant with given product variant id {body.product_variant_id} doesnot exist")
    max_quantity=exist_product.stock_level
    role=exist_user.role


    if body.quantity > max_quantity:
               raise HTTPException(
                      status_code=status.HTTP_400_BAD_REQUEST,
                      detail=f"max quantity is {max_quantity} "
               )
    data=body.model_dump()
    new_cart=Cart(user_id=user.id,product_id=body.product_id,product_variant_id=body.product_variant_id,quantity=data["quantity"])

    if role !="user":
           raise HTTPException(
                  status_code=404,
                  detail="only users can create carts"
           )

    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return{
           "status":"cart created successfully",
           "data": new_cart
    }

def get_cart(db:Session,user:User):
       carts=db.query(Cart).filter(Cart.user_id==user.id).all()
       if not carts:
              raise HTTPException(status_code=404,detail="Cart not found")
       return carts

def update_cart(body:cartUpdateBase,cart_id,db:Session,user:User):
       carts:Cart=db.query(Cart).filter(Cart.id== cart_id).first()
       if not carts:
              raise HTTPException(status_code=404,detail=f"cart with id {cart_id} does not exist ")

       if carts.user_id != user.id:
              raise HTTPException (404,detail=f" you are not allowed to update this cart  ")
       

       body=body.model_dump()
       for field,value in body.items():
              setattr(carts,field,value)

       db.add(carts)
       db.commit()
       db.refresh(carts)

       return carts