from fastapi import FastAPI

from atm_machines.database import db


def create_app() -> FastAPI:
    app = FastAPI()

    @app.on_event("startup")
    async def startup():
        await db.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await db.disconnect()

    return app
