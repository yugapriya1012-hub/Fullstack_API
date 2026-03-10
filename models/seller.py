from sqlalchemy import Column, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship

class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    products = relationship("Product", back_populates="seller")