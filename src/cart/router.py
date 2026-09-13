from fastapi import APIRouter,Depends
from src.cart.dtos import cartBase,cartUpdateBase
from src.cart import controller
from src.utils.db import get_db
from src.user.is_auth import is_authenticated
from sqlalchemy.orm import Session
from src.user.models import User


cart_routes=APIRouter(prefix="/cart")

@cart_routes.post("/create_cart")
def create_cart(body:cartBase,db:Session=Depends(get_db),user=Depends(is_authenticated)):
    return controller.create_cart(body,db,user)

@cart_routes.get("/get_cart")
def get_cart(db:Session=Depends(get_db),user:User=Depends(is_authenticated)):
    return controller.get_cart(db,user)

@cart_routes.put("/update_cart/{cart_id}",response_model=cartBase)
def update_cart(body:cartUpdateBase,cart_id:int,db:Session=Depends(get_db),user:User=Depends(is_authenticated)):
    return controller.update_cart(body,cart_id,db,user)

@cart_routes.delete("/delete_cart/{cart_id}")
def delete_product_cart(cart_id:int,db:Session=Depends(get_db),user:User=Depends(is_authenticated)):
    return controller.delete_cart(cart_id,db,user)