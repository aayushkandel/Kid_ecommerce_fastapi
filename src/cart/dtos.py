from pydantic import BaseModel

class cartBase(BaseModel):
    
    product_id:int
    product_variant_id: int | None=None
    quantity:int

class cartUpdateBase(BaseModel):
    product_id:int
    product_variant_id:int
    quantity:int



