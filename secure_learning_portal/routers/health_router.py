from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(tags=["System"])

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "secure-learning-portal",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
