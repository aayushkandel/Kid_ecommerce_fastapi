from pydantic import BaseModel

class ProductsBase(BaseModel):
    category_id:int
    name:str
    slug:str
    description:str
    price:int
    stock_level:int

class ProductsResponseBase(BaseModel):
    message:str = "Product created successfully "
    id:int
    name:str
    category_id:int

class ProductsUpdateResponseBase(BaseModel):
    message:str = "Product updated successfully "
    id:int
    name:str
    category_id:int

class GalleryResponse(BaseModel):
    message: str
    product_id: int
    product_name: str
    images: list[str]


    

