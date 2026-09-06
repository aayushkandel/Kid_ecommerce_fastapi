from pydantic import BaseModel

class ProductsBase(BaseModel):
    category_id:int
    product_variant_id: int | None=None
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

class AllProductsResponseBase(BaseModel):
    
    id: int
    name: str
    category: str
    slug: str
    price: float
    stock_level: int

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


    

