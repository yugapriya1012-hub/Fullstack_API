from pydantic import BaseModel

class OrderItemCreate(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: float

class OrderItemOut(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float
    product_name: str
