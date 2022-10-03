import databases
import sqlalchemy

from atm_machines.config import settings

db = databases.Database(settings.DB_URI)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


engine = sqlalchemy.create_engine(settings.DB_URI, connect_args={"check_same_thread": False})
metadata.create_all(engine)
