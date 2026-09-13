from pydantic import BaseModel
from typing import Literal,List

class getorder(BaseModel):
    user_id:int
    cart_id:int
    amout:int
    order_status:str
    remarks:str
    cancel_reason:str
    

class createOrder(BaseModel):
    user_id:int
    cart_id:int
    remarks:str



class PaymentBase(BaseModel):
    payment_method: Literal["esewa", "khalti"]
    transaction_id: str | None = None

class OrderItemResponse(BaseModel):
    product_name: str
    cart_id: int
    quantity: int
    rate: int


class OrderResponse(BaseModel):
    order_id: int
    amount: int
    order_status: str
    order_items: List[OrderItemResponse]

class CancelOrder(BaseModel):
    order_id:int
    remarks:str | None = None
    cancel_reason:str