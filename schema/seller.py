from pydantic import BaseModel
from typing import Optional

class SellerCreate(BaseModel):
    name: str
    email: str
    password: str
    phone: str

class SellerLogin(BaseModel):
    email: str
    password: str

class SellerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None

class Config:
        from_attributes = True   


