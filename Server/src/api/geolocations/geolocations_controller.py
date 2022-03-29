from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.geolocations.dto import GeolocationDto, CreateGeolocationDto
from api.config import Settings, get_settings
from .geolocations_service import find_all, create, find_one_by_ip, find_one_by_url
from api.database import get_db
from api.utils import HTTP_EXCEPTIONS

router = APIRouter()

maybe_string = str | None


@router.get("/geolocations", response_model=list[GeolocationDto])
def read_geolocations(db: Session = Depends(get_db)):
    return find_all(db)


@router.get("/geolocation", response_model=GeolocationDto)
def find_geolocation_by_ip_or_url(
    ip: maybe_string = None, url: maybe_string = None, db: Session = Depends(get_db)
):
    if (ip and url) or (ip and url) == False:
        raise HTTPException(**HTTP_EXCEPTIONS[460])

    return find_one_by_ip(db, ip) if ip else find_one_by_url(db, url)


@router.post("/geolocations", response_model=GeolocationDto, status_code=201)
def create_geolocation(
    request_body: CreateGeolocationDto,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    return create(request_body, db, settings)
