from pydantic import BaseModel

class ProductVarientBase(BaseModel):
    variant_name:str
    variant_value:str
    description:str