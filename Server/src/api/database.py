import logging

from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from api.config import get_settings


log = logging.getLogger(__name__)

try:
    engine = create_engine(get_settings().database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except SQLAlchemyError as e:
    log.error(e)


@as_declarative()
class Base:
    def _asdict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def db_healthcheck():
    try:
        engine.table_names()
    except Exception:
        return False
    return True
