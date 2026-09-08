from src.products.dtos import ProductsBase,AddRates
from sqlalchemy.orm import Session
from src.products.models import Products,ProductRate
from fastapi import HTTPException
from src.products.models import ProductGallery
from src.products.gallery import upload_product_image
from src.category.models import Category
from src.product_varients.models import ProductVariant



def create_product(body:ProductsBase,db:Session):

    exist_category=db.query(Category).filter(Category.id==body.category_id).first()
    if not exist_category:
        raise HTTPException(status_code=404,detail=f"Category id {body.category_id} doesnot exist")
   
    data=body.model_dump()
    new_task=Products(name=data["name"], slug=data["slug"], description=data["description"],price=data["price"],stock_level=data["stock_level"],category_id=body.category_id)

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
            "description":product.description,
            "category": product.category.name,
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

def get_all_images(db: Session):

    galleries = (
        db.query(ProductGallery, Products)
        .join(Products, ProductGallery.product_id == Products.id)
        .all()
    )

    result = {}

    for gallery, product in galleries:

        if product.id not in result:
            result[product.id] = {
                "product_id": product.id,
                "product_name": product.name,
                "images": []
            }

        result[product.id]["images"].append({
            "id": gallery.id,
            "image": gallery.image
        })

    return list(result.values())

def delete_product_image(image_id:int,db:Session):
    image=db.query(ProductGallery).filter(ProductGallery.id==image_id).first()
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


def addProductRates(body: AddRates, db: Session):

    new_rate = ProductRate(
        rate=body.rate,
        stock_level=body.stock_level,
        product_id=body.product_id,
        product_variant_id=body.product_variant_id
    )

    db.add(new_rate)
    db.commit()
    db.refresh(new_rate)

    return {
        "id": new_rate.id,

        "product_id": new_rate.product_id,
        "product_name": new_rate.products.name
            if new_rate.products else None,

        "product_variant_id": new_rate.product_variant_id,

        "variant_name": new_rate.product_variants.variant_name
            if new_rate.product_variants else None,

        "variant_value": new_rate.product_variants.variant_value
            if new_rate.product_variants else None,

        "rate": new_rate.rate,
        "stock_level": new_rate.stock_level
    }

def getProductRates(db: Session):

    rates = (
        db.query(ProductRate)
        .join(Products, ProductRate.product_id == Products.id)
        .outerjoin(
            ProductVariant,
            ProductRate.product_variant_id == ProductVariant.id
        )
        .all()
    )

    data = []

    for rate in rates:
        data.append({
            "id": rate.id,
            "product_id": rate.product_id,
            "product_name": rate.products.name if rate.products else None,

            "product_variant_id": rate.product_variant_id,
            "variant_name": (
                rate.product_variants.variant_name
                if rate.product_variants
                else None
            ),
            "variant_value": (
                rate.product_variants.variant_value
                if rate.product_variants
                else None
            ),

            "rate": rate.rate,
            "stock_level": rate.stock_level
        })

    return {
        "data": data
    }

def updateProductRates(body: AddRates,product_id: int,product_variant_id: int,db: Session):
    rate_data = db.query(ProductRate).filter(ProductRate.product_id == product_id,ProductRate.product_variant_id == product_variant_id).first()

    if not rate_data:
        raise HTTPException(
            status_code=404,
            detail="Product rate not found"
        )

    rate_data.rate = body.rate
    rate_data.stock_level = body.stock_level

    db.commit()
    db.refresh(rate_data)

    return rate_data

def deleteProductRates(product_id:int,product_variant_id:int,db:Session):
    delRates = db.query(ProductRate).filter(ProductRate.product_id == product_id,ProductRate.product_variant_id == product_variant_id).first()
    
    if not delRates:
            raise HTTPException(
                status_code=404,
                detail="Product rate not found"
            )

    db.delete(delRates)
    db.commit()

    return{"message":"Rates deleted successfully"}