from src.category.dtos import CategoryBase
from sqlalchemy.orm import Session
from src.category.models import Category
from fastapi import HTTPException,status

def create_category(body:CategoryBase,db:Session):

    exist_category=db.query(Category).filter(Category.name== body.name).first()
    if exist_category:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Category with name {body.name} already exist")
    data=body.model_dump()
    new_category=Category(name=data["name"], slug=data["slug"],description=data["description"])

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return {
        "message":"Category created successfully",
        "id":new_category.id,
        "name":new_category.name,
        "slug":new_category.slug,
        "description":new_category.description
    }

def get_category(db:Session):
    categories=db.query(Category).all()

    return {
        "status":"All categories",
        "data":categories
    }

def get_one_category(category_id:int,db:Session):
    one_category=db.query(Category).get(category_id)
    if not one_category:
        raise HTTPException(
            status_code=404,
            detail="No category found"
        )
    return{
        "status":"Category fetched successfully",
        "data":one_category
    }

def update_category(body:CategoryBase,category_id:int, db:Session):
    one_category=db.query(Category).get(category_id)
    if not one_category:
        raise HTTPException(
            status_code=404,
            detail="category not found"
        )
    body=body.model_dump()
    for field,value in body.items():
        setattr(one_category,field,value)

    db.add(one_category)
    db.commit()
    db.refresh(one_category)

    return{
        "status": "category updated successfully",
        "data":one_category

    }

def delete_category(category_id:int,db:Session):
    one_category=db.query(Category).get(category_id)
    if not one_category:
             raise HTTPException(
                 status_code=404,
                 detail="No category found"
             )
    db.delete(one_category)
    db.commit()
 
    return {"status":"Category deleted successfully"}