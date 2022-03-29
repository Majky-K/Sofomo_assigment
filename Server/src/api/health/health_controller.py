from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.config import Settings, get_settings
from api.database import db_healthcheck

router = APIRouter()


class HealthDto(BaseModel):
    is_ok: bool
    environment: str
    testing: str


@router.get("/health", response_model=HealthDto)
def health(settings: Settings = Depends(get_settings)):
    return {
        "is_ok": True and db_healthcheck(),
        "environment": settings.environment,
        "testing": settings.testing,
    }
