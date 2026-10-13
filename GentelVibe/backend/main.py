from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import uuid

from database import Base, engine, get_db
from models import User, Product, Order, OrderItem
from schemas import (
    ProductOut, ProductCreate,
    OrderCreate, OrderOut, StatusUpdate,
    UserLogin, Token, UserRegister, CustomerLogin
)
from auth import (
    hash_password, verify_password,
    create_access_token, get_current_admin
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="GentleVibe API", version="2.5.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_order_code() -> str:
    return "GV" + uuid.uuid4().hex[:8].upper()


# ---------------- Auth ----------------
@app.post("/api/register")
@app.post("/api/auth/register")
def register_customer(payload: UserRegister, db: Session = Depends(get_db)):
    email_clean = payload.email.strip().lower()
    if db.query(User).filter((User.username == email_clean) | (User.email == email_clean)).first():
        raise HTTPException(status_code=400, detail="An account with this email already exists.")

    new_user = User(
        full_name=payload.fullName.strip(),
        username=email_clean,
        email=email_clean,
        phone=payload.phone.strip(),
        hashed_password=hash_password(payload.password),
        is_admin=0
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_access_token({"sub": new_user.username})
    return {
        "success": True,
        "token": token,
        "user": {
            "fullName": new_user.full_name,
            "email": new_user.email,
            "phone": new_user.phone
        }
    }


@app.post("/api/login")
@app.post("/api/auth/customer-login")
def login_customer(payload: CustomerLogin, db: Session = Depends(get_db)):
    email_clean = payload.email.strip().lower()
    user = db.query(User).filter((User.username == email_clean) | (User.email == email_clean)).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token({"sub": user.username})
    return {
        "success": True,
        "token": token,
        "user": {
            "fullName": user.full_name or user.username,
            "email": user.email,
            "phone": user.phone
        }
    }


@app.post("/api/auth/login", response_model=Token)
def login_admin(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/api/auth/me")
def me(admin: User = Depends(get_current_admin)):
    return {"username": admin.username, "is_admin": bool(admin.is_admin)}


# ---------------- Products ----------------
@app.get("/api/products", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.get("/api/products/{code}", response_model=ProductOut)
def get_product(code: str, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.code == code).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p


# ---------------- Orders ----------------
def _order_to_dict(o: Order) -> dict:
    return {
        "id": o.id,
        "order_code": o.order_code,
        "customerName": o.customer_name,
        "customerPhone": o.customer_phone,
        "customerEmail": o.customer_email,
        "shippingAddress": o.shipping_address,
        "paymentMethod": o.payment_method or "COD",
        "paymentTrxId": o.payment_trx_id or "N/A",
        "paymentDetails": o.payment_details or "N/A",
        "totalAmount": o.total_amount,
        "status": o.status,
        "createdAt": o.created_at.isoformat(),
        "items": [
            {
                "id": it.id,
                "name": it.product_name,
                "code": it.product_code,
                "price": it.price,
                "quantity": it.quantity,
                "size": it.size,
                "image": it.image
            }
            for it in o.items
        ]
    }


@app.post("/api/orders", response_model=OrderOut, status_code=201)
def place_order(payload: OrderCreate, db: Session = Depends(get_db)):
    if not payload.items:
        raise HTTPException(status_code=400, detail="Order must contain items")

    order = Order(
        order_code=generate_order_code(),
        customer_name=payload.customerName,
        customer_phone=payload.customerPhone,
        customer_email=payload.customerEmail or "",
        shipping_address=payload.shippingAddress,
        payment_method=payload.paymentMethod or "COD",
        payment_trx_id=payload.paymentTrxId or "",
        payment_details=payload.paymentDetails or "",
        total_amount=payload.totalAmount,
        status="Pending"
    )
    db.add(order)
    db.flush()

    for item in payload.items:
        db.add(OrderItem(
            order_id=order.id,
            product_name=item.name,
            product_code=item.code or "",
            size=item.size,
            price=item.price,
            quantity=item.quantity,
            image=item.image or ""
        ))

    db.commit()
    db.refresh(order)
    return _order_to_dict(order)


@app.get("/api/orders", response_model=List[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).order_by(Order.id.desc()).all()
    return [_order_to_dict(o) for o in orders]


@app.get("/api/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = None
    if order_id.isdigit():
        order = db.query(Order).filter(Order.id == int(order_id)).first()
    if not order:
        order = db.query(Order).filter(Order.order_code == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _order_to_dict(order)


@app.patch("/api/orders/{order_id}")
def update_status(order_id: str, payload: StatusUpdate, db: Session = Depends(get_db)):
    order = None
    if order_id.isdigit():
        order = db.query(Order).filter(Order.id == int(order_id)).first()
    if not order:
        order = db.query(Order).filter(Order.order_code == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if payload.status not in ("Pending", "Delivered", "Cancelled"):
        raise HTTPException(status_code=400, detail="Invalid status")

    order.status = payload.status
    db.commit()
    return {"message": "Status updated", "status": order.status}


@app.delete("/api/orders/{order_id}")
def delete_order(order_id: str, db: Session = Depends(get_db)):
    order = None
    if order_id.isdigit():
        order = db.query(Order).filter(Order.id == int(order_id)).first()
    if not order:
        order = db.query(Order).filter(Order.order_code == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted"}


@app.delete("/api/orders")
def clear_all_orders(db: Session = Depends(get_db)):
    db.query(OrderItem).delete()
    db.query(Order).delete()
    db.commit()
    return {"message": "All orders cleared"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)