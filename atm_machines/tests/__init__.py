from sqlalchemy import func

from atm_machines.atms.models import LONG_LAT_SRID

TEST_LONG = 10.01
TEST_LAT = 89.91
TEST_GEOGRAPHY = func.ST_SetSRID(func.ST_MakePoint(TEST_LONG, TEST_LAT), LONG_LAT_SRID)

TEST_ENDPOINT = "/v1/atms/"
