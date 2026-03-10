# from pydantic import BaseModel
# from datetime import datetime
# from typing import List


# class OrderItemCreate(BaseModel):
#     product_id: int
#     quantity: int

# class OrderItemOut(BaseModel):
#     product_id: int
#     quantity: int
#     price: float
#     product_name: str


# class OrderCreate(BaseModel):
#     customer_id: int
#     items: List[OrderItemCreate]

# class OrderOut(BaseModel):
#     id: int
#     customer_id: int
#     total_amount: float
#     status: str
#     created_at: datetime
#     items: List[OrderItemOut]

# class OrderUpdate(BaseModel):
#     status: str


from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price: float
    product_name: str

class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]
    delivery_date: Optional[date] = None 

# class OrderOut(BaseModel):
#     id: int
#     customer_id: int
#     total_amount: float
#     status: str
#     created_at: datetime
#     delivery_date: Optional[date] = None 
#     items: List[OrderItemOut]

class OrderOut(BaseModel):
    id: int
    customer_id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    status: str


