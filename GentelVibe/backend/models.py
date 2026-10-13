from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, default="")
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, default="")
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Integer, default=0)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    brand = Column(String, default="GentleVibe")
    description = Column(Text, default="")
    price = Column(Float, nullable=False)
    image = Column(String, default="")
    category = Column(String, default="T-Shirt")
    stock = Column(Integer, default=100)
    rating = Column(Float, default=5.0)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_code = Column(String, unique=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    customer_email = Column(String, default="")
    shipping_address = Column(Text, nullable=False)
    total_amount = Column(Float, nullable=False)
    
    # Payment fields
    payment_method = Column(String, default="COD")       # COD, bKash, Nagad, Rocket, Bank, Visa
    payment_trx_id = Column(String, default="")          # TrxID / Deposit Slip / Authorization Code
    payment_details = Column(String, default="")         # Optional: Bank account or masked card info
    
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_name = Column(String)
    product_code = Column(String, default="")
    size = Column(String, default="Standard")
    price = Column(Float)
    quantity = Column(Integer)
    image = Column(String, default="")
    order = relationship("Order", back_populates="items")