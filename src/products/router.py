from fastapi import APIRouter,Depends,status,UploadFile,File
from src.products import controller
from src.products.dtos import ProductsBase,ProductsResponseBase,GalleryResponse,ProductsUpdateResponseBase,AddRates
from src.utils.db import get_db
from typing import List
from sqlalchemy.orm import Session
from src.user.is_auth import is_admin_authenticated
from src.user.models import User




product_routes=APIRouter(prefix="/products")

@product_routes.post("/create_product",response_model=ProductsResponseBase,status_code=status.HTTP_201_CREATED)
def create_product(body:ProductsBase,db:Session=Depends(get_db),admin=Depends(is_admin_authenticated)):

    return controller.create_product(body,db)

@product_routes.get("/all_products",status_code=status.HTTP_200_OK)
def get_all_products(db:Session=Depends(get_db),admin=Depends(is_admin_authenticated)):
    return controller.get_products(db)

@product_routes.get("/one_product/{product_id}",response_model=ProductsResponseBase,status_code=status.HTTP_200_OK)
def get_one_product(product_id:int,db:Session=Depends(get_db),data=Depends(is_admin_authenticated)):
    return controller.get_one_product(product_id,db)


@product_routes.put("/update/{product_id}",response_model=ProductsUpdateResponseBase,status_code=status.HTTP_201_CREATED)
def update_product(body:ProductsBase,product_id:int, db:Session=Depends(get_db),admin=Depends(is_admin_authenticated)):
    return controller.update_product(body,product_id,db)

@product_routes.delete("/delete/{product_id}")
def delete_product(product_id:int,db:Session=Depends(get_db),admin=Depends(is_admin_authenticated)):
    return controller.delete_product(product_id,db)

@product_routes.post("/upload/{product_id}",response_model=GalleryResponse)
def upload_images(product_id: int,images: List[UploadFile] = File(...),db: Session = Depends(get_db),admin=Depends(is_admin_authenticated)):
    return controller.upload_gallery_images(product_id,images,db)

@product_routes.get("/get_images/{product_id}")
def get_images(product_id:int,db:Session=Depends(get_db),admin=Depends(is_admin_authenticated)):
    return controller.get_product_images(product_id,db)

@product_routes.delete("/delete_image/{image_id}")
def delete_image(image_id:int, db:Session=Depends(get_db),admin=Depends(is_admin_authenticated)):
    return controller.delete_product_image(image_id,db)

# for products rates

@product_routes.post("/add_rates")
def postRates(body:AddRates,db:Session=Depends(get_db)):
    return controller.addProductRates(body,db)

@product_routes.get("/all_rates",status_code=status.HTTP_200_OK)
def getRates(db:Session=Depends(get_db)):
    return controller.getProductRates(db)

@product_routes.put("/update_rates/{product_id}/{product_variant_id}",status_code=status.HTTP_201_CREATED)
def updateRates(body:AddRates,product_id:int,product_variant_id:int,db:Session=Depends(get_db)):
    return controller.updateProductRates(body,product_id,product_variant_id,db)

@product_routes.delete("/delete_rates/{product_id}/{product_variant_id}",status_code=status.HTTP_200_OK)
def deleteRates(product_id:int,product_variant_id:int,db:Session=Depends(get_db)):
    return controller.deleteProductRates(product_id,product_variant_id,db)