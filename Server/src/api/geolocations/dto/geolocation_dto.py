from pydantic import BaseModel


class GeolocationDto(BaseModel):
    ip: str
    type: str
    continent_code: str
    continent_name: str
    country_code: str
    country_name: str
    region_code: str
    region_name: str
    city: str
    zip: str
    url: str | None
