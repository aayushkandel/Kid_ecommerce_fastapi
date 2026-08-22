from src.product_varients.dtos import ProductVarientBase
from sqlalchemy.orm import Session
from src.product_varients.models import ProductVariant
from fastapi import HTTPException
from src.products.models import Products


def create_product_varients(body:ProductVarientBase,db:Session):
    exist_product=db.query(Products).filter(Products.id==body.product_id).first()

    if not exist_product:
        raise HTTPException(status_code=404,detail=f"Product with given product id {body.product_id} doesnot exist")
    data=body.model_dump()
    new_product_varients=ProductVariant(product_id=body.product_id,variant_name=data["variant_name"], variant_type=data["variant_type"], variant_value=data["variant_value"], description=data["description"])

    db.add(new_product_varients)
    db.commit()
    db.refresh(new_product_varients)
    return{
        "status":"Product varient created successfully",
        "data":new_product_varients
    }

def get_product_varients(db:Session):
    products_varients=db.query(ProductVariant).all()

    return{
        "status":"All products",
        "data":products_varients
    }

def get_one_product_varient(product_id:int,db:Session):
    one_product_varients=db.query(ProductVariant).get(product_id)
    if not one_product_varients:
        raise HTTPException(
            status_code=404,
            detail="no product varient found "
        )
    return{
        "status":"producted fetched successfully","data":one_product_varients
    }

def update_product_varient(body:ProductVarientBase, product_id:int,db:Session):
    one_product_varients=db.query(ProductVariant).get(product_id)
    if not one_product_varients:
        raise HTTPException(
            status_code=404,
            detail="No product found"
        )

    body=body.model_dump()
    for field, value in body.items():
        setattr(one_product_varients,field,value)
    # one_product_varients.name=body.name
    # one_product_varients.slug=body.slug
    # one_product_varients.description=body.description

    db.add(one_product_varients)
    db.commit()
    db.refresh(one_product_varients)

    return{
        "status":"data updated successfully","data":one_product_varients
    }


def delete_product_varient(product_id:int, db:Session):
    one_product_varients=db.query(ProductVariant).get(product_id)
    if not one_product_varients:
            raise HTTPException(
                status_code=404,
                detail="No product found"
            )
    db.delete(one_product_varients)
    db.commit()

    return {"status":"data deleted successfully"}