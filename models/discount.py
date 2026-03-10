from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from db.database import Base

class Discount(Base):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    discount_type = Column(String)  # percentage 
    value = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
