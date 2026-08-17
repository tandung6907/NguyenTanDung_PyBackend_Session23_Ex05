from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from dependencies.authentication import get_current_user
from models.models import ResourceModel
from schemas.schemas import ResourceResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/my-resources", response_model=list[ResourceResponse])
def my_resources(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(ResourceModel).filter(
        ResourceModel.owner_id == current_user.id
    ).all()
