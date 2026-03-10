from pydantic import BaseModel
from datetime import datetime

class ReviewCreate(BaseModel):
    rating: int
    comment: str
    product_id: int

class ReviewUpdate(BaseModel):
    rating: int
    comment: str

class ReviewOut(BaseModel):
    id: int
    rating: int
    comment: str
    customer_name: str
    created_at: datetime

