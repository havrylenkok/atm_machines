from fastapi import FastAPI

from atm_machines.atms.api import atms_api
from atm_machines.config import settings


def create_app() -> FastAPI:
    app = FastAPI(debug=settings.ENV_NAME == "local")

    app.include_router(atms_api, prefix="/v1")

    return app
