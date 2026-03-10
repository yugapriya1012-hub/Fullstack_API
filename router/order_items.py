from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.order_items import OrderItem
from models.product import Product
from schema.order_items import OrderItemCreate, OrderItemOut

router = APIRouter(prefix="/order-items", tags=["Order Items"])

@router.post("/", response_model=OrderItemOut)
def add_order_item(data: OrderItemCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    order_item = OrderItem(
        order_id=data.order_id,
        product_id=data.product_id,
        quantity=data.quantity,
        price=data.price
    )
    db.add(order_item)
    db.commit()
    db.refresh(order_item)

    return OrderItemOut(
        id=order_item.id,
        order_id=order_item.order_id,
        product_id=order_item.product_id,
        quantity=order_item.quantity,
        price=order_item.price,
        product_name=product.product_name
    )


@router.get("/", response_model=list[OrderItemOut])
def get_order_items(db: Session = Depends(get_db)):
    items = db.query(OrderItem).all()
    result = []
    for i in items:
        result.append(OrderItemOut(
            id=i.id,
            order_id=i.order_id,
            product_id=i.product_id,
            quantity=i.quantity,
            price=i.price,
            product_name=i.product.product_name
        ))
    return result


# @router.get("/{item_id}", response_model=OrderItemOut)
# def get_order_item(item_id: int, db: Session = Depends(get_db)):
#     item = db.query(OrderItem).filter(OrderItem.id == item_id).first()
#     if not item:
#         raise HTTPException(status_code=404, detail="Order item not found")
#     return OrderItemOut(
#         id=item.id,
#         order_id=item.order_id,
#         product_id=item.product_id,
#         quantity=item.quantity,
#         price=item.price,
#         product_name=item.product.product_name
#     )
@router.get("/by-order/{order_id}", response_model=list[OrderItemOut])
def get_items_by_order(order_id: int, db: Session = Depends(get_db)):
    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    result = []
    for i in items:
        result.append(OrderItemOut(
            id=i.id,
            order_id=i.order_id,
            product_id=i.product_id,
            quantity=i.quantity,
            price=i.price,
            product_name=i.product.product_name
        ))
    return result

@router.put("/{item_id}", response_model=OrderItemOut)
def update_order_item(item_id: int, data: OrderItemCreate, db: Session = Depends(get_db)):
    item = db.query(OrderItem).filter(OrderItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")

    item.order_id = data.order_id
    item.product_id = data.product_id
    item.quantity = data.quantity
    item.price = data.price

    db.commit()
    db.refresh(item)

    product = db.query(Product).filter(Product.id == item.product_id).first()

    return OrderItemOut(
        id=item.id,
        order_id=item.order_id,
        product_id=item.product_id,
        quantity=item.quantity,
        price=item.price,
        product_name=product.product_name
    )
