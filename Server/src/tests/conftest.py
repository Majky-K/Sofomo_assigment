import os
from api.config import get_settings, Settings

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.main import app, create_application
from api.database import Base, get_db

engine = create_engine(os.getenv("DATABASE_TEST_URL"))
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def test_app():
    app.dependency_overrides[get_settings] = get_settings_override
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)
