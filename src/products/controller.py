from src.products.dtos import ProductsBase
from sqlalchemy.orm import Session
from src.products.models import Products
from fastapi import HTTPException
from src.products.models import ProductGallery
from src.products.gallery import upload_product_image
from src.category.models import Category



def create_product(body:ProductsBase,db:Session):

    exist_category=db.query(Category).filter(Category.id==body.category_id).first()
    if not exist_category:
        raise HTTPException(status_code=404,detail=f"Category id {body.category_id} doesnot exist")

    exist_product=db.query(Products).filter(Products.name==body.name).first()

    if exist_product:
       raise HTTPException(status_code=404, detail=f" Product {body.name} already exist.")
    data=body.model_dump()
    new_task=Products(name=data["name"], slug=data["slug"], description=data["description"],price=data["price"],stock_level=data["stock_level"],category_id=body.category_id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_products(db:Session):
    products=db.query(Products).all()  

    return products

def get_one_product(product_id:int,db:Session):
    one_product=db.query(Products).get(product_id)
    if not one_product:
        raise HTTPException(
            status_code=404,
            detail="No product found"
        )
    return one_product

def update_product(body:ProductsBase, product_id:int,db:Session):
    one_product=db.query(Products).get(product_id)
    if not one_product:
        raise HTTPException(
            status_code=404,
            detail="No product found"
        )

    body=body.model_dump()
    for field, value in body.items():
        setattr(one_product,field,value)
    # one_product.name=body.name
    # one_product.slug=body.slug
    # one_product.description=body.description

    db.add(one_product)
    db.commit()
    db.refresh(one_product)

    return one_product


def delete_product(product_id:int, db:Session):
    one_product=db.query(Products).get(product_id)
    if not one_product:
            raise HTTPException(
                status_code=404,
                detail="No product found"
            )
    db.delete(one_product)
    db.commit()

    return {
        "message":"Product deleted Successfully"
    }


def upload_gallery_images(product_id: int,images,db: Session):

    # Find product
    product = db.query(Products).filter(Products.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product does not exist"
        )

    uploaded_images = []

    for image in images:

        # Save physical image
        image_path = upload_product_image(
            product_id=product.id,
            product_name=product.name,
            image=image
        )

        # Save image path in database
        gallery_image = ProductGallery(
            product_id=product.id,
            image=image_path
        )

        db.add(gallery_image)

        uploaded_images.append(image_path)

    db.commit()

    return {
        "message": "Images uploaded successfully",
        "product_id": product.id,
        "product_name": product.name,
        "images": uploaded_images
    }

def get_product_images(product_id:int,db:Session):
    images=db.query(ProductGallery).filter(ProductGallery.product_id==product_id).all()
    if not images:
        raise HTTPException(
            status_code=404,
            detail=f"Image for product id {product_id} is not found "
        )
    return  {
        "messages":f"images of product id {product_id}",
        "images":images
    }

def delete_product_image(image_id:int,db:Session):
    image=db.query(ProductGallery).get(image_id)
    if not image:
        raise HTTPException(
            status_code=404,
            detail=f"No image with image id {image_id} is found"
        )
    db.delete(image)
    db.commit()

    return{
        "message":"Image deleted successfully"
    }
    