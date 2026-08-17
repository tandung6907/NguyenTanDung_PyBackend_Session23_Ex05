from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from models.models import UserModel
from schemas.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from security.security import create_access_token, verify_password
from services.auth_service import register_user
from dependencies.authentication import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(db, data)

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()

    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def current_user(current_user=Depends(get_current_user)):
    return current_user
