from pydantic import BaseModel

class CustomerCreate(BaseModel):
    name: str
    email: str
    password: str
    phone: str


class CustomerOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str

class CustomerLogin(BaseModel):
    email: str
    password: str
    class Config:
          from_attributes = True
