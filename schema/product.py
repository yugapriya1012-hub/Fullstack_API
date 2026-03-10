from pydantic import BaseModel

class ProductResponse(BaseModel):
    id: int
    seller_id: int
    product_name: str
    description: str
    price: float
    places: str
    discount: int
    image: str

    class Config:
        from_attributes = True
