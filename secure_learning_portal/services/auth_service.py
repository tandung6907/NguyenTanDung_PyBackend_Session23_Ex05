from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.models import UserModel
from schemas.schemas import RegisterRequest
from security.security import hash_password

def register_user(db: Session, data: RegisterRequest):
    existing_user = db.query(UserModel).filter(UserModel.email == data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    user = UserModel(
        email=data.email,
        password_hash=hash_password(data.password),
        full_name=data.full_name.strip(),
        role="user",
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
