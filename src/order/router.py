from fastapi import APIRouter, Depends,status
from src.order import controller
from src.user.is_auth import is_authenticated
from src.utils.db import get_db
from sqlalchemy.orm import Session
from src.order.dtos import PaymentBase,CancelOrder
from src.user.models import User

order_routes=APIRouter(prefix="/order")

@order_routes.post("/create_order")
def create_order(db:Session=Depends(get_db),user=Depends(is_authenticated)):
    return controller.my_order(db,user)

@order_routes.post("/payment")
def make_payment(body: PaymentBase,db: Session = Depends(get_db),user: User = Depends(is_authenticated)):
    return controller.create_payment(body,db,user)

@order_routes.put("/cancel_reason/")
def cancel_order(body:CancelOrder,db:Session=Depends(get_db),user:User=Depends(is_authenticated)):
    return controller.cancel_order(body,db,user)

@order_routes.get("/getmyorder")
def getOrder(db:Session=Depends(get_db),user:User=Depends(is_authenticated)):
    return controller.getMyOrder(db,user)

@order_routes.delete("/deletemyorder/{order_id}")
def deleteOrder(order_id: int, db: Session = Depends(get_db), user: User = Depends(is_authenticated)):
    return controller.deleteMyOrder(db, user, order_id)