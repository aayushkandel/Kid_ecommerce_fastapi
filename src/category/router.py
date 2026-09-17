from fastapi import APIRouter, Depends
from src.category import controller
from src.category.dtos import CategoryBase
from src.utils.db import get_db
from src.user.is_auth import is_admin_authenticated

category_routes=APIRouter(prefix="/categories")

@category_routes.post("/create_category")
def create_category(body:CategoryBase,db=Depends(get_db) ):
    return controller.create_category(body,db)

@category_routes.get("/all_category")
def get_all_categories(db=Depends(get_db)):
    return controller.get_category(db)

@category_routes.get("/one_category/{category_id}")
def get_one_category(category_id:int,db=Depends(get_db),admin= Depends(is_admin_authenticated)):
    return controller.get_one_category(category_id, db)

@category_routes.put("/update_category/{category_id}")
def update_category(body:CategoryBase,category_id:int,db=Depends(get_db),admin= Depends(is_admin_authenticated)):
    return controller.update_category(body,category_id,db)

@category_routes.delete("/delete_category/{category_id}")
def delete_category(category_id:int,db=Depends(get_db),admin= Depends(is_admin_authenticated)):
    return controller.delete_category(category_id,db)