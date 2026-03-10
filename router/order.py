from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.order import Order
from typing import List
from models.order_items import OrderItem
from models.product import Product
from models.customer import Customer
from schema.order import OrderCreate, OrderOut, OrderItemOut, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])

# 1. CREATE ORDER
@router.post("/", response_model=OrderOut)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == data.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    order = Order(customer_id=data.customer_id, delivery_date=data.delivery_date)
    db.add(order)
    db.commit()
    db.refresh(order)

    total_amount = 0
    items_out = []

    for item in data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price * item.quantity
        )
        db.add(order_item)
        total_amount += order_item.price

        items_out.append(OrderItemOut(
            product_id=product.id,
            quantity=item.quantity,
            price=order_item.price,
            product_name=product.product_name
        ))

    order.total_amount = total_amount
    db.commit()
    db.refresh(order)
    return OrderOut(
        id=order.id, customer_id=order.customer_id, total_amount=order.total_amount,
        status=order.status, created_at=order.created_at, delivery_date=order.delivery_date,
        items=items_out
    )

# 2. CUSTOMER ORDERS (Used by My Orders Page)
@router.get("/customer/{customer_id}", response_model=List[OrderOut])
def get_customer_orders(customer_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.customer_id == customer_id).order_by(Order.created_at.desc()).all()
    
    result = []
    for order in orders:
        items_list = [
            OrderItemOut(
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
                product_name=item.product.product_name 
            ) for item in order.order_items
        ]
        result.append(OrderOut(
            id=order.id, customer_id=order.customer_id, total_amount=order.total_amount,
            status=order.status, created_at=order.created_at, delivery_date=order.delivery_date,
            items=items_list
        ))
    return result

# 3. SELLER ORDERS (Used by Order Management Page)
@router.get("/seller/{seller_id}", response_model=List[OrderOut])
def get_seller_orders(seller_id: int, db: Session = Depends(get_db)):
    # Join queries to filter orders belonging to a specific seller
    orders = db.query(Order).join(OrderItem).join(Product).filter(Product.seller_id == seller_id).distinct().all()
    
    result = []
    for order in orders:
        # Filter only the items that belong to THIS seller
        seller_items = [
            OrderItemOut(
                product_id=i.product_id,
                quantity=i.quantity,
                price=i.price,
                product_name=i.product.product_name
            ) for i in order.order_items if i.product.seller_id == seller_id
        ]
        result.append(OrderOut(
            id=order.id, customer_id=order.customer_id, total_amount=order.total_amount,
            status=order.status, created_at=order.created_at, delivery_date=order.delivery_date,
            items=seller_items
        ))
    return result

# 4. UPDATE ORDER STATUS
@router.put("/{order_id}", response_model=OrderOut)
def update_order_status(order_id: int, data: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = data.status
    db.commit()
    db.refresh(order)
    
    items_out = [
        OrderItemOut(
            product_id=i.product_id, quantity=i.quantity, 
            price=i.price, product_name=i.product.product_name
        ) for i in order.order_items
    ]
    return OrderOut(
        id=order.id, customer_id=order.customer_id, total_amount=order.total_amount, 
        status=order.status, created_at=order.created_at, 
        delivery_date=order.delivery_date, items=items_out
    )

# 5. GET CUSTOMER BY EMAIL
@router.get("/by-email")
def get_customer_by_email(email: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.email == email).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer