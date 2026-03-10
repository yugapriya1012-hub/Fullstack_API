from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base
from models.order import Order

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    amount = Column(Float, nullable=False)
    payment_method = Column(String)  # UPI, CARD, CASH, NETBANKING
    status = Column(String, default="pending")  # pending, success, failed
    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order")