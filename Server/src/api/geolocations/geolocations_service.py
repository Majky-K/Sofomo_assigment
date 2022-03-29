from fastapi import HTTPException
from sqlalchemy.orm import Session
from api.geolocations.dto import GeolocationDto, CreateGeolocationDto
from api.utils import HTTP_EXCEPTIONS

from .utils import get_response_or_404, obtain_geolocation_info
from . import GeoLocation


def find_all(db: Session):
    return [geolocation._asdict() for geolocation in db.query(GeoLocation).all()]


def find_one_by_ip(db: Session, ip: str):
    query_result = db.query(GeoLocation).filter_by(ip=ip).first()
    print(db.query(GeoLocation).filter_by(ip="1.1.1.1"))
    return get_response_or_404(query_result)


def find_one_by_url(db: Session, url: str):
    query_result = db.query(GeoLocation).filter_by(url=url).first()
    return get_response_or_404(query_result)


def create(request_body: CreateGeolocationDto, db: Session, settings) -> GeolocationDto:
    geolocation_info = obtain_geolocation_info(request_body, settings)

    already_exist = (
        db.query(GeoLocation).filter_by(ip=geolocation_info["ip"]).first()
        if request_body.__root__.type == "ip"
        else db.query(GeoLocation).filter_by(ip=geolocation_info["url"]).first()
    )

    if already_exist:
        raise HTTPException(**HTTP_EXCEPTIONS["461"])

    geolocation = GeoLocation(**geolocation_info)
    db.add(geolocation)
    db.commit()
    db.refresh(geolocation)

    return geolocation._asdict()
