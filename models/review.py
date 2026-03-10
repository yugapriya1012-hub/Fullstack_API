from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)        # 1 to 5
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    customer = relationship("Customer", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")
