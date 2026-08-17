from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from dependencies.authentication import get_current_user
from models.models import ResourceModel
from schemas.schemas import ResourceCreate, ResourceResponse, ResourceUpdate
from services.resource_service import create_resource, get_resource, update_resource

router = APIRouter(prefix="/resources", tags=["Resources"])

@router.get("", response_model=list[ResourceResponse])
def list_resources(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(ResourceModel).filter(
        ResourceModel.owner_id == current_user.id
    ).all()

@router.post("", response_model=ResourceResponse, status_code=201)
def create(
    data: ResourceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_resource(db, data, current_user.id)

@router.get("/{resource_id}", response_model=ResourceResponse)
def get_one(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    resource = get_resource(db, resource_id)

    if current_user.role != "admin" and resource.owner_id != current_user.id:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this resource"
        )

    return resource

@router.put("/{resource_id}", response_model=ResourceResponse)
def update(
    resource_id: int,
    data: ResourceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    resource = get_resource(db, resource_id)

    if current_user.role != "admin" and resource.owner_id != current_user.id:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this resource"
        )

    return update_resource(db, resource_id, data)
