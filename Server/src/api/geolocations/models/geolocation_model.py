from sqlalchemy import Column, String

from api.database import Base


class GeoLocation(Base):
    __tablename__ = "geo_location"

    ip = Column(String, primary_key=True, index=True)
    type = Column(String, index=True)
    continent_code = Column(String, index=True)
    continent_name = Column(String, index=True)
    country_code = Column(String, index=True)
    country_name = Column(String, index=True)
    region_code = Column(String, index=True)
    region_name = Column(String, index=True)
    city = Column(String, index=True)
    zip = Column(String, index=True)
    url = Column(String, index=True, nullable=True)
