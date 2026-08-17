from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.models import ResourceModel
from schemas.schemas import ResourceCreate, ResourceUpdate

def create_resource(db: Session, data: ResourceCreate, owner_id: int):
    resource = ResourceModel(
        title=data.title,
        description=data.description,
        resource_type=data.resource_type,
        owner_id=owner_id
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource

def get_resource(db: Session, resource_id: int):
    resource = db.query(ResourceModel).filter(ResourceModel.id == resource_id).first()
    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    return resource

def update_resource(db: Session, resource_id: int, data: ResourceUpdate):
    resource = get_resource(db, resource_id)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(resource, key, value)

    db.commit()
    db.refresh(resource)
    return resource

def delete_resource(db: Session, resource_id: int):
    resource = get_resource(db, resource_id)
    db.delete(resource)
    db.commit()
