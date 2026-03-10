from pydantic import BaseModel
from datetime import datetime

class DiscountCreate(BaseModel):
    code: str
    discount_type: str   # percentage
    value: float
    expires_at: datetime   # REQUIRED

class DiscountUpdate(BaseModel):
    is_active: bool

class DiscountOut(BaseModel):
    id: int
    code: str
    discount_type: str
    value: float
    is_active: bool
    expires_at: datetime   # REQUIRED
    created_at: datetime
