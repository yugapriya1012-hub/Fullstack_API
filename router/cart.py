from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.cart import Cart
from models.product import Product
from models.customer import Customer
from schema.cart import CartCreate, CartOut, CartUpdate

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/", response_model=CartOut)
def add_to_cart(data: CartCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_item = Cart(
        customer_id=data.customer_id,
        product_id=data.product_id,
        quantity=data.quantity
    )
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return CartOut(
        id=cart_item.id,
        customer_id=cart_item.customer_id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity,
        created_at=cart_item.created_at,
        product_name=product.product_name,
        price=product.price
    )




@router.get("/{customer_id}", response_model=list[CartOut])
def get_cart(customer_id: int, db: Session = Depends(get_db)):
    items = db.query(Cart).filter(Cart.customer_id == customer_id).all()
    result = []

    for item in items:
        result.append(CartOut(
            id=item.id,
            customer_id=item.customer_id,
            product_id=item.product_id,
            quantity=item.quantity,
            created_at=item.created_at,
            product_name=item.product.product_name,
            price=item.product.price,
            image=item.product.image 
        ))
    return result


@router.put("/{cart_id}", response_model=CartOut)
def update_cart(cart_id: int, data: CartUpdate, db: Session = Depends(get_db)):
    cart_item = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.quantity = data.quantity
    db.commit()
    db.refresh(cart_item)

    return CartOut(
        id=cart_item.id,
        customer_id=cart_item.customer_id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity,
        created_at=cart_item.created_at,
        product_name=cart_item.product.product_name,
        price=cart_item.product.price
    )


@router.delete("/{cart_id}")
def delete_cart_item(cart_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"message": "Cart item removed successfully"}
