import uuid

from geoalchemy2 import Geography
from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID

from atm_machines.database import Base

LONG_LAT_SRID = 4326


class AtmModel(Base):
    __tablename__ = "atms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    address = Column(String)
    provider = Column(String)

    geography = Column(Geography(geometry_type="POINT", srid=LONG_LAT_SRID))
