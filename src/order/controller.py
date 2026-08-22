from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from src.user.models import User
from src.cart.models import Cart
from src.products.models import Products
from src.order.models import Order,OrderItem,Payment
from src.order.dtos import PaymentBase,OrderItemResponse,CancelOrder,OrderResponse

def my_order(db: Session, user: User):

    # Get all carts belonging to this user
    carts = db.query(Cart).filter(
        Cart.user_id == user.id
    ).all()

    if not carts:
        raise HTTPException(
            status_code=404,
            detail="Cart is empty"
        )

    # Get cart IDs that have ALREADY been converted into order items
    ordered_cart_ids = db.query(
        OrderItem.cart_id
    ).join(
        Order,
        Order.id == OrderItem.order_id
    ).filter(
        Order.user_id == user.id
    ).all()

    # Convert [(1,), (2,), (3,)] into {1, 2, 3}
    ordered_cart_ids = {
        cart_id[0] for cart_id in ordered_cart_ids
    }

    # Keep ONLY carts that have never been ordered
    new_carts = [
        cart for cart in carts
        if cart.id not in ordered_cart_ids
    ]

    if not new_carts:
        raise HTTPException(
            status_code=400,
            detail="No new cart items to order"
        )

    # Create a new order
    order = Order(
        user_id=user.id,
        amount=0,
        order_status="pending"
    )

    db.add(order)
    db.flush()

    total_amount = 0
    order_items_response=[]

    # Create order items ONLY for new carts
    for cart in new_carts:

        product = db.query(Products).filter(
            Products.id == cart.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {cart.product_id} does not exist"
            )

        rate = product.price
        quantity = cart.quantity

        item_amount = rate * quantity

        order_item = OrderItem(
            product_id=cart.product_id,
            product_variant_id=cart.product_variant_id,
            order_id=order.id,
            cart_id=cart.id,
            quantity=quantity,
            rate=rate
        )

        db.add(order_item)

        total_amount += item_amount
        order_items_response.append(
            OrderItemResponse(
                product_name=product.name,
                cart_id=cart.id,
                quantity=quantity,
                rate=rate
            )
        )

    order.amount = total_amount

    db.commit()
    db.refresh(order)

    return OrderResponse(
        order_id=order.id,
        amount=order.amount,
        order_status=order.order_status,
        order_items=order_items_response
    )

def create_payment(body: PaymentBase,db: Session,user: User):
    
    # Find pending order of logged-in user
    order = db.query(Order).filter(Order.user_id == user.id,Order.order_status == "pending").order_by(Order.id.desc()).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="No pending order found"
        )

    # Check whether this order is already paid
    existing_payment = db.query(Payment).filter(
        Payment.order_id == order.id,
        Payment.payment_status == "paid"
    ).first()

    if existing_payment:
        raise HTTPException(
            status_code=400,
            detail="Payment already completed for this order"
        )

    # Amount comes directly from order
    amount = order.amount

    # Create payment
    payment = Payment(
        user_id=user.id,
        order_id=order.id,
        payment_method=body.payment_method,
        amount=amount,
        transaction_id=body.transaction_id,
        payment_status="paid"
    )

    db.add(payment)

    # Complete the order
    order.order_status = "completed"

    db.commit()

    db.refresh(payment)
    db.refresh(order)

    return {
        "message": "Payment successful",
        "payment": payment,
        "order": order
    }

def cancel_order(body:CancelOrder,db:Session,user:User):
    exist_order=db.query(Order).filter(Order.id==body.order_id).first()
    if not exist_order:
        raise HTTPException(status_code=404,detail=f"Order no {body.order_id}  not found")

    if exist_order.user_id !=user.id:
        raise HTTPException(status_code=404,detail="You are not allowed to cancel this order")

    if exist_order.order_status=="completed":
        raise HTTPException (status_code=400,  detail="completed order can't be cancelled")

    exist_order.order_status="Canceled"
    exist_order.remarks=body.remarks
    exist_order.cancel_reason=body.cancel_reason


    
    db.commit()
    db.refresh(exist_order)

    return exist_order 


