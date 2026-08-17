from database.database import Base, SessionLocal, engine
from models.models import ResourceModel, UserModel
from security.security import hash_password

Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    admin = db.query(UserModel).filter(UserModel.email == "admin@example.com").first()
    user = db.query(UserModel).filter(UserModel.email == "user@example.com").first()

    if admin is None:
        admin = UserModel(
            email="admin@example.com",
            password_hash=hash_password("Admin@123"),
            full_name="System Admin",
            role="admin",
            is_active=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

    if user is None:
        user = UserModel(
            email="user@example.com",
            password_hash=hash_password("User@123"),
            full_name="Demo User",
            role="user",
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    if db.query(ResourceModel).count() == 0:
        db.add_all([
            ResourceModel(
                title="Python FastAPI Basics",
                description="Tài liệu nhập môn FastAPI và REST API.",
                resource_type="document",
                owner_id=user.id
            ),
            ResourceModel(
                title="JWT Authentication",
                description="Tài liệu về JWT và xác thực người dùng.",
                resource_type="document",
                owner_id=user.id
            )
        ])
        db.commit()
finally:
    db.close()

print("Seed completed")
print("Admin: admin@example.com / Admin@123")
print("User: user@example.com / User@123")
