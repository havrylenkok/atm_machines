from fastapi import APIRouter

from atm_machines.atms import endpoints

atms_api = APIRouter()
atms_api.include_router(endpoints.router, tags=["atms"])
