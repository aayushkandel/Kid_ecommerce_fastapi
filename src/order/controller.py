from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from src.user.models import User
from src.cart.models import Cart
from src.products.models import Products,ProductRate
from src.order.models import Order,OrderItem,Payment
from src.order.dtos import PaymentBase,OrderItemResponse,CancelOrder,OrderResponse



# ============================================================
# CREATE ORDER FROM CART
# ============================================================

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

    # ========================================================
    # GET CART IDs WHOSE ORDER PAYMENT IS ALREADY COMPLETED
    # ========================================================

    completed_order_cart_ids = db.query(
        OrderItem.cart_id
    ).join(
        Order,
        Order.id == OrderItem.order_id
    ).join(
        Payment,
        Payment.order_id == Order.id
    ).filter(
        Order.user_id == user.id,
        Payment.payment_status == "paid"
    ).all()

    completed_order_cart_ids = {
        cart_id[0]
        for cart_id in completed_order_cart_ids
        if cart_id[0] is not None
    }

    # ========================================================
    # ONLY REMOVE CARTS WHOSE PAYMENT IS COMPLETED
    # ========================================================

    new_carts = [
        cart
        for cart in carts
        if cart.id not in completed_order_cart_ids
    ]

    if not new_carts:
        raise HTTPException(
            status_code=400,
            detail="No cart items available for order"
        )

    # ========================================================
    # CREATE ORDER
    # ========================================================

    order = Order(
        user_id=user.id,
        amount=0,
        order_status="pending"
    )

    db.add(order)
    db.flush()

    total_amount = 0
    order_items_response = []

    # ========================================================
    # CREATE ORDER ITEMS
    # ========================================================

    for cart in new_carts:

        product = db.query(Products).filter(
            Products.id == cart.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {cart.product_id} does not exist"
            )

        # Default product price
        rate = product.price

        variant_name = None
        variant_value = None

        # ====================================================
        # IF CART HAS VARIANT
        # ====================================================

        if cart.product_variant_id is not None:

            product_rate = db.query(ProductRate).filter(
                ProductRate.product_id == cart.product_id,
                ProductRate.product_variant_id == cart.product_variant_id
            ).first()

            if not product_rate:
                raise HTTPException(
                    status_code=404,
                    detail=(
                        f"Variant rate not found for "
                        f"product {cart.product_id}"
                    )
                )

            rate = product_rate.rate

            variant = product_rate.product_variants

            if variant:
                variant_name = variant.variant_name
                variant_value = variant.variant_value

        # ====================================================
        # CALCULATE AMOUNT
        # ====================================================

        quantity = cart.quantity

        item_amount = rate * quantity

        # ====================================================
        # CREATE ORDER ITEM
        # ====================================================

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

    # ========================================================
    # SET TOTAL ORDER AMOUNT
    # ========================================================

    order.amount = total_amount

    db.commit()
    db.refresh(order)

    return OrderResponse(
        order_id=order.id,
        amount=order.amount,
        order_status=order.order_status,
        order_items=order_items_response
    )


# ============================================================
# PAYMENT
# ============================================================

def create_payment(
    body: PaymentBase,
    db: Session,
    user: User
):

    # Get latest pending order
    order = db.query(Order).filter(
        Order.user_id == user.id,
        Order.order_status == "pending"
    ).order_by(
        Order.id.desc()
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="No pending order found"
        )

    # Check whether this order has already been paid
    existing_payment = db.query(Payment).filter(
        Payment.order_id == order.id,
        Payment.payment_status == "paid"
    ).first()

    if existing_payment:
        raise HTTPException(
            status_code=400,
            detail="Payment already completed for this order"
        )

    # Amount comes from order
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

    # Complete order
    order.order_status = "completed"

    # ========================================================
    # GET CART ITEMS BELONGING TO THIS ORDER
    # ========================================================

    order_items = db.query(OrderItem).filter(
        OrderItem.order_id == order.id
    ).all()

    # ========================================================
    # DELETE ORDERED CART ITEMS
    # ========================================================

    for order_item in order_items:

        if order_item.cart_id is not None:

            cart = db.query(Cart).filter(
                Cart.id == order_item.cart_id,
                Cart.user_id == user.id
            ).first()

            if cart:
                db.delete(cart)

    # ========================================================
    # SAVE PAYMENT + ORDER + CART DELETION
    # ========================================================

    db.commit()

    db.refresh(payment)
    db.refresh(order)

    return {
        "message": "Payment successful",
        "payment": payment,
        "order": order
    }


# ============================================================
# CANCEL ORDER
# ============================================================

def cancel_order(
    body: CancelOrder,
    db: Session,
    user: User
):

    exist_order = db.query(Order).filter(
        Order.id == body.order_id
    ).first()

    if not exist_order:
        raise HTTPException(
            status_code=404,
            detail=f"Order no {body.order_id} not found"
        )

    # Make sure order belongs to logged-in user
    if exist_order.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to cancel this order"
        )

    # Completed order cannot be cancelled
    if exist_order.order_status == "completed":
        raise HTTPException(
            status_code=400,
            detail="Completed order can't be cancelled"
        )

    # Already cancelled
    if exist_order.order_status == "canceled":
        raise HTTPException(
            status_code=400,
            detail="Order is already canceled"
        )

    exist_order.order_status = "canceled"
    exist_order.remarks = body.remarks
    exist_order.cancel_reason = body.cancel_reason

    db.commit()
    db.refresh(exist_order)

    return {
        "message": "Order canceled successfully",
        "order": exist_order
    }


# ============================================================
# GET MY ORDERS
# ============================================================

def getMyOrder(db: Session, user: User):

    orders = (
        db.query(Order)
        .filter(Order.user_id == user.id)
        .order_by(Order.id.desc())
        .all()
    )

    if not orders:
        raise HTTPException(
            status_code=404,
            detail="order not found"
        )

    result = []

    for order in orders:

        payment = (
            db.query(Payment)
            .filter(Payment.order_id == order.id)
            .order_by(Payment.id.desc())
            .first()
        )

        order_items = (
            db.query(OrderItem)
            .filter(OrderItem.order_id == order.id)
            .all()
        )

        items = []

        for item in order_items:

            product = (
                db.query(Products)
                .filter(Products.id == item.product_id)
                .first()
            )

            items.append({
                "id": item.id,
                "cart_id": item.cart_id,
                "product_id": item.product_id,
                "product_variant_id": item.product_variant_id,
                "product_name": (
                    product.name
                    if product
                    else "Product unavailable"
                ),
                "quantity": item.quantity,
                "rate": float(item.rate),
            })

        result.append({
            "order_id": order.id,
            "amount": float(order.amount),
            "order_status": order.order_status,
            "remarks": order.remarks,
            "cancel_reason": order.cancel_reason,
            "created_at": order.created_at,
            "payment_status": (
                payment.payment_status
                if payment
                else "pending"
            ),
            "payment_method": (
                payment.payment_method
                if payment
                else None
            ),
            "order_items": items,
        })

    return result


# ============================================================
# DELETE MY ORDER
# ============================================================

def deleteMyOrder(
    db: Session,
    user: User,
    order_id: int
):

    # IMPORTANT:
    # Use Order.id, not order.id
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="No order found"
        )

    if order.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to delete this order"
        )

    db.delete(order)
    db.commit()

    return {
        "message": "Order deleted successfully"
    }