from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)

    product_name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    places = Column(String, nullable=False)
    discount = Column(Integer, nullable=False)
    image = Column(String, nullable=False)   # stores filename or path

    seller = relationship("Seller", back_populates="products")
    reviews = relationship("Review", back_populates="product")