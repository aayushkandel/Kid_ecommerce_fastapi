from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
from src.products import models
from src.utils.db import engine,get_db,Base
from sqlalchemy.orm import Session
from src.products.router import product_routes
from src.category.router import category_routes
from src.product_varients.router import product_varient_routes
from src.user.router import user_router
from src.cart.router import cart_routes
from src.order.router import order_routes
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app=FastAPI()

app.mount("/gallery", StaticFiles(directory="gallery"), name="gallery")

origins=['http://localhost:5173']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(product_routes)
app.include_router(category_routes)
app.include_router(product_varient_routes)
app.include_router(user_router)
app.include_router(order_routes)
app.include_router(cart_routes)

Base.metadata.create_all(engine)






