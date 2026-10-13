from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# ---------- PRODUCT ----------
class ProductBase(BaseModel):
    code: str
    name: str
    brand: str = "GentleVibe"
    description: str = ""
    price: float
    image: str = ""
    category: str = "T-Shirt"
    stock: int = 100
    rating: float = 5.0


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True


# ---------- ORDER ITEM ----------
class OrderItemIn(BaseModel):
    name: str
    code: Optional[str] = ""
    price: float
    quantity: int
    size: str = "Standard"
    image: Optional[str] = ""


class OrderItemOut(OrderItemIn):
    id: int

    class Config:
        from_attributes = True


# ---------- ORDER ----------
class OrderCreate(BaseModel):
    customerName: str
    customerPhone: str
    customerEmail: Optional[str] = ""
    shippingAddress: str
    paymentMethod: Optional[str] = "COD"
    paymentTrxId: Optional[str] = ""
    paymentDetails: Optional[str] = ""
    items: List[OrderItemIn]
    totalAmount: float


class OrderOut(BaseModel):
    id: int
    order_code: str
    customerName: str
    customerPhone: str
    customerEmail: str
    shippingAddress: str
    paymentMethod: str
    paymentTrxId: str
    paymentDetails: str
    totalAmount: float
    status: str
    createdAt: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True


class StatusUpdate(BaseModel):
    status: str


# ---------- AUTH ----------
class UserRegister(BaseModel):
    fullName: str
    email: str
    phone: str
    password: str


class CustomerLogin(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"