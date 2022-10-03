from fastapi import APIRouter

from atm_machines.atms import endpoints

api_router = APIRouter()
api_router.include_router(endpoints.router, tags=["atms"])
