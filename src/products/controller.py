from src.products.dtos import ProductsBase
from sqlalchemy.orm import Session
from src.products.models import Products
from fastapi import HTTPException
from src.products.models import ProductGallery
from src.products.gallery import upload_product_image
from src.category.models import Category
from src.product_varients.models import ProductVariant



def create_product(body:ProductsBase,db:Session):

    exist_category=db.query(Category).filter(Category.id==body.category_id).first()
    if not exist_category:
        raise HTTPException(status_code=404,detail=f"Category id {body.category_id} doesnot exist")
    if body.product_variant_id is not None:
        exist_product_variant=db.query(ProductVariant).filter(ProductVariant.id==body.product_variant_id)
        if not exist_product_variant:
                raise HTTPException(status_code=404,detail=f"product variant id {body.product_variant_id} doesnot exist")
    data=body.model_dump()
    new_task=Products(name=data["name"], slug=data["slug"], description=data["description"],price=data["price"],stock_level=data["stock_level"],category_id=body.category_id,product_variant_id=body.product_variant_id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_products(db:Session):
    products=db.query(Products).all()  

    return [
        {
            "id": product.id,
            "name": product.name,
            "category_id":product.category_id,
            "product_variant_id": product.product_variant_id or None,

            
            "description":product.description,
            "category": product.category.name,
           "product_variant_name": (
            product.product_variants.variant_name
            if product.product_variants
            else None
        ),

        "product_variant_value": (
            product.product_variants.variant_value
            if product.product_variants
            else None
        ),

            "slug": product.slug,
            "price": product.price,
            "stock_level": product.stock_level,
        }
        for product in products
    ]

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
    