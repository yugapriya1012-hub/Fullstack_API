from pydantic import BaseModel
from datetime import datetime

class CartCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int

class CartUpdate(BaseModel):
    quantity: int

class CartOut(BaseModel):
    id: int
    customer_id: int
    product_id: int
    quantity: int
    created_at: datetime
    product_name: str
    price: float

    