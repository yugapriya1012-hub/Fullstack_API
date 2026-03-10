from pydantic import BaseModel
from datetime import datetime

class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    payment_method: str

class PaymentUpdate(BaseModel):
    status: str

class PaymentOut(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_method: str
    status: str
    created_at: datetime
