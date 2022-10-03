import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker

from atm_machines.config import settings

engine = sqlalchemy.create_engine(settings.DB_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
