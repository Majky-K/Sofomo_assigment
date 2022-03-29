import logging
from fastapi import FastAPI, Depends

from api.auth import auth_controller
from api.auth.auth_bearer import JWTBearer
from api.models import models
from api.database import engine
from api.geolocations import geolocations_controller

from api.health import health_controller

log = logging.getLogger("uvicorn")
logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    application = FastAPI(
        title="Sofomo assigment api",
        description="Welcome to Sofomo's assigment API documentation! Here you will able to discover all of the ways "
                    "you can interact with the Sofomo API.",
    )
    application.include_router(health_controller.router, tags=["System"])
    application.include_router(auth_controller.router, tags=["Auth"])
    application.include_router(
        geolocations_controller.router,
        tags=["Geolocations"],
        dependencies=[Depends(JWTBearer())],
    )

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    try:
        models.Base.metadata.create_all(bind=engine)
    except Exception as e:
        logger.error(e)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
