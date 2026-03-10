from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.payment import Payment
from models.order import Order
from schema.payment import PaymentCreate, PaymentOut, PaymentUpdate

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=PaymentOut)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    payment = Payment(
        order_id=data.order_id,
        amount=data.amount,
        payment_method=data.payment_method
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


@router.get("/", response_model=list[PaymentOut])
def get_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()


@router.get("/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.put("/{payment_id}", response_model=PaymentOut)
def update_payment(payment_id: int, data: PaymentUpdate, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    payment.status = data.status
    db.commit()
    db.refresh(payment)

    return payment
