from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from dependencies import get_db
from models.discount import Discount
from schema.discount import DiscountCreate, DiscountOut, DiscountUpdate

router = APIRouter(prefix="/discounts", tags=["Discounts"])


@router.post("/", response_model=DiscountOut)
def create_discount(data: DiscountCreate, db: Session = Depends(get_db)):
    existing = db.query(Discount).filter(Discount.code == data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Discount code already exists")

    discount = Discount(
        code=data.code,
        discount_type=data.discount_type,
        value=data.value,
        expires_at=data.expires_at
    )
    db.add(discount)
    db.commit()
    db.refresh(discount)
    return discount


@router.get("/", response_model=list[DiscountOut])
def get_discounts(db: Session = Depends(get_db)):
    return db.query(Discount).all()


@router.get("/{code}", response_model=DiscountOut)
def get_discount(code: str, db: Session = Depends(get_db)):
    discount = db.query(Discount).filter(Discount.code == code).first()
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    return discount


@router.put("/{discount_id}", response_model=DiscountOut)
def update_discount(discount_id: int, data: DiscountUpdate, db: Session = Depends(get_db)):
    discount = db.query(Discount).filter(Discount.id == discount_id).first()
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")

    discount.is_active = data.is_active
    db.commit()
    db.refresh(discount)
    return discount


@router.post("/apply/{code}")
def apply_discount(code: str, amount: float, db: Session = Depends(get_db)):
    discount = db.query(Discount).filter(
        Discount.code == code,
        Discount.is_active == True
    ).first()

    if not discount:
        raise HTTPException(status_code=404, detail="Invalid discount code")

    if discount.expires_at and discount.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Discount expired")

    if discount.discount_type == "percentage":
        discount_amount = (amount * discount.value) / 100
    else:
        discount_amount = discount.value

    final_amount = max(amount - discount_amount, 0)

    return {
        "original_amount": amount,
        "discount": discount_amount,
        "final_amount": final_amount
    }
