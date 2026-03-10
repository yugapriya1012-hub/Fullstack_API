# from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from db.database import Base


# class Order(Base):
#     __tablename__ = "orders"

#     id = Column(Integer, primary_key=True, index=True)
#     customer_id = Column(Integer, ForeignKey("customers.id"))
#     total_amount = Column(Float, default=0.0)
#     status = Column(String, default="pending")  # pending, completed, canceled
#     created_at = Column(DateTime, default=datetime.utcnow)

#     customer = relationship("Customer")
#     order_items = relationship("OrderItem", back_populates="order")


from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    total_amount = Column(Float, default=0.0)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    delivery_date = Column(Date, nullable=True)  

    customer = relationship("Customer")
    order_items = relationship("OrderItem", back_populates="order")