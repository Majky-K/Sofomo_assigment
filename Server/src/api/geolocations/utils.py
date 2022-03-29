import logging
import requests
from fastapi import Depends, HTTPException
from pydantic import HttpUrl

from api.config import Settings, get_settings
from api.utils import HTTP_EXCEPTIONS
from api.geolocations.dto import CreateGeolocationDto
from requests.adapters import HTTPAdapter, Retry

from . import GeoLocation


s = requests.Session()
retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])

log = logging.getLogger(__name__)


def get_response_or_404(query_result: GeoLocation | None):
    if query_result:
        return query_result._asdict()
    raise HTTPException(404)


def obtain_geolocation_info(
    data: CreateGeolocationDto, settings: Settings = Depends(get_settings)
):
    print(settings.ip_api_key, settings.testing)
    uri = (
        data.__root__.value.host
        if isinstance(data.__root__.value, HttpUrl)
        else data.__root__.value
    )
    s.mount("http://", HTTPAdapter(max_retries=retries))

    try:
        res = s.get(f"http://api.ipstack.com/{uri}?access_key={settings.ip_api_key}")
        response = res.json()
    except Exception as e:
        log.error(e)
        raise HTTPException(404)

    if "error" in response:
        raise HTTPException(404, detail=response["error"]["info"])

    if response["continent_code"] is None:
        raise HTTPException(**HTTP_EXCEPTIONS["462"])

    if data.__root__.type == "url":
        response["url"] = data.__root__.value

    # todo ask recruiter what is really needed and simplify code
    omitKeys = (
        "latitude",
        "longitude",
        "location",
        "time_zone",
        "currency",
        "connection",
        "security",
    )
    new_response = {k: v for k, v in response.items() if k not in omitKeys}
    return new_response
