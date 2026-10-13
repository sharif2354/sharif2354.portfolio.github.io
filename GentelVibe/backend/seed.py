from database import SessionLocal, Base, engine
from models import User, Product
from auth import hash_password

PRODUCTS = [
    ("TEE-001", "Cartoon Astronaut Tee", 78.00, "T-Shirt",
     "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop",
     "Organic cotton tee with a playful astronaut print."),
    ("TEE-002", "Tropical Palm Shirt", 78.00, "Shirt",
     "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500&auto=format&fit=crop",
     "Breathable tropical shirt perfect for warm days."),
    ("TEE-003", "Floral Print Shirt", 78.00, "Shirt",
     "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=500&auto=format&fit=crop",
     "Soft floral print with a relaxed fit."),
    ("TEE-004", "Vintage Pink Tee", 78.00, "T-Shirt",
     "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&auto=format&fit=crop",
     "Faded pink vintage look with modern comfort."),
    ("TEE-005", "Ocean Breeze Tee", 78.00, "T-Shirt",
     "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500&auto=format&fit=crop",
     "Cool and refreshing ocean-inspired design."),
    ("TEE-006", "Sunset Stripe Tee", 78.00, "T-Shirt",
     "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=500&auto=format&fit=crop",
     "Striped design inspired by warm summer sunsets."),
    ("TEE-007", "Desert Sand Shirt", 78.00, "Shirt",
     "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=500&auto=format&fit=crop",
     "Earthy tone shirt with premium stitching."),
    ("TEE-008", "Coastal Linen Shirt", 78.00, "Shirt",
     "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=500&auto=format&fit=crop",
     "Lightweight linen blend for coastal getaways.")
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if not db.query(User).filter(User.username == "admin").first():
            db.add(User(
                full_name="System Administrator",
                username="admin",
                email="admin@gentlevibe.com",
                hashed_password=hash_password("admin123"),
                is_admin=1
            ))
            print("[seed] Admin user created -> admin / admin123")

        if db.query(Product).count() == 0:
            for code, name, price, cat, img, desc in PRODUCTS:
                db.add(Product(
                    code=code, name=name, price=price,
                    category=cat, image=img, description=desc
                ))
            print(f"[seed] {len(PRODUCTS)} products inserted")

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()