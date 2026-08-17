from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from dependencies.authorization import require_admin
from models.models import ResourceModel, UserModel
from schemas.schemas import AdminUserResponse, ResourceResponse
from services.resource_service import delete_resource

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=list[AdminUserResponse])
def get_users(
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    return db.query(UserModel).all()

@router.patch("/users/{user_id}/lock", response_model=AdminUserResponse)
def lock_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.is_active = False
    db.commit()
    db.refresh(user)
    return user

@router.get("/resources", response_model=list[ResourceResponse])
def get_all_resources(
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    return db.query(ResourceModel).all()

@router.delete("/resources/{resource_id}", status_code=204)
def delete(
    resource_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    delete_resource(db, resource_id)
