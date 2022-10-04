from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, conint


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
    distance: Optional[int]


class AtmsReadParams(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]
    radius: Optional[conint(ge=0, le=2000)] = 50  # type: ignore
    offset: Optional[conint(ge=0)] = 0  # type: ignore
    limit: Optional[conint(ge=0, le=2000)] = 50  # type: ignore
