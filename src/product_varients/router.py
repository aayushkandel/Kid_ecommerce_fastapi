from fastapi import APIRouter,Depends
from src.product_varients import controller
from src.product_varients.dtos import ProductVarientBase
from src.utils.db import get_db
from src.user.is_auth import is_admin_authenticated



product_varient_routes=APIRouter(prefix="/products_varients")

@product_varient_routes.post("/create_product_varients")
def create_product_varients(body:ProductVarientBase,db=Depends(get_db),admin=Depends(is_admin_authenticated)):
    return controller.create_product_varients(body,db)

@product_varient_routes.get("/all_product_varients")
def get_all_product_varients(db=Depends(get_db),data=Depends(is_admin_authenticated)):
    return controller.get_product_varients(db)

@product_varient_routes.get("/one_product_varient/{product_id}")
def get_one_product_varients(product_id:int,db=Depends(get_db),data=Depends(is_admin_authenticated)):
    return controller.get_one_product_varient(product_id,db)


@product_varient_routes.put("/update_procuct_varient/{product_id}")
def update_product_varient(body:ProductVarientBase,product_id:int, db=Depends(get_db),data=Depends(is_admin_authenticated)):
    return controller.update_product_varient(body,product_id,db)

@product_varient_routes.delete("/delete_product_varient/{product_id}")
def delete_product_varient(product_id,db=Depends(get_db),data=Depends(is_admin_authenticated)):
    return controller.delete_product_varient(product_id,db)