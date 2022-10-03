from typing import List

from geoalchemy2 import Geometry
from sqlalchemy import cast, func
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from atm_machines.atms.models import LONG_LAT_SRID, AtmModel
from atm_machines.atms.schemas import AtmCreateParams, AtmsReadParams


class AtmsController:
    def __init__(self, db: Session):
        self.db = db

    def read_atms(self, params: AtmsReadParams) -> List[Row]:
        optional_columns = []
        point = None
        if params.longitude and params.latitude:
            point = func.ST_Point(params.longitude, params.latitude)

            optional_columns.append(func.ST_Distance(AtmModel.geography, point).label("distance"))

        query = self.db.query(
            AtmModel.id,
            AtmModel.created_at,
            AtmModel.address,
            AtmModel.provider,
            func.ST_Y(cast(AtmModel.geography, Geometry)).label("latitude"),
            func.ST_X(cast(AtmModel.geography, Geometry)).label("longitude"),
            *optional_columns,
        )

        if point is not None:
            query = query.filter(func.ST_DWithin(AtmModel.geography, point, params.radius))

        query = query.order_by("id").limit(params.limit).offset(params.offset).all()

        return query

    def create_atm(self, params: AtmCreateParams) -> AtmModel:
        data = params.dict()
        data.pop("longitude")
        data.pop("latitude")
        data["geography"] = func.ST_SetSRID(
            func.ST_MakePoint(params.longitude, params.latitude), LONG_LAT_SRID
        )

        atm = AtmModel(**data)

        self.db.add(atm)
        self.db.commit()
        self.db.refresh(atm)

        return atm
