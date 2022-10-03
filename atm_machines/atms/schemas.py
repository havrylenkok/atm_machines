from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel


class AtmBase(BaseModel):
    address: str
    provider: str
    latitude: Optional[float]
    longitude: Optional[float]


class AtmShort(BaseModel):
    id: UUID4
    created_at: datetime

    class Config:
        orm_mode = True


class AtmCreateParams(AtmBase):
    pass


class Atm(AtmBase):
    id: UUID4
    created_at: datetime


class AtmsReadParams(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]
    radius: Optional[int] = 50
    offset: Optional[int] = 0
    limit: Optional[int] = 50
