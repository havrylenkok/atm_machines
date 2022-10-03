from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from atm_machines.atms.controllers import AtmsController
from atm_machines.atms.schemas import Atm, AtmCreateParams, AtmShort, AtmsReadParams
from atm_machines.dependencies import get_db

router = APIRouter()


@router.get("/atms/", response_model=List[Atm])
def read_atms(params: AtmsReadParams = Depends(), db: Session = Depends(get_db)):
    return AtmsController(db).read_atms(params)


@router.post("/atms/", response_model=AtmShort)
def create_atm(params: AtmCreateParams, db: Session = Depends(get_db)):
    return AtmsController(db).create_atm(params)
