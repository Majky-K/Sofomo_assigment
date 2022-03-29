from typing import Literal
from pydantic import BaseModel, IPvAnyAddress, HttpUrl, Field


class CreateGeolocationIpDto(BaseModel):
    type: Literal["ip"]
    value: IPvAnyAddress


class CreateGeolocationUrlDto(BaseModel):
    type: Literal["url"]
    value: HttpUrl


class CreateGeolocationDto(BaseModel):
    __root__: CreateGeolocationIpDto | CreateGeolocationUrlDto = Field(
        ..., discriminator="type"
    )

    class Config:
        schema_extra = {
            "example": {
                "type": "ip or url",
                "value": "string"
            }
        }
