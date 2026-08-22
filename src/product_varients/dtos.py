from pydantic import BaseModel

class ProductVarientBase(BaseModel):
    product_id: int
    variant_name:str
    variant_type:str
    variant_value:str
    description:str