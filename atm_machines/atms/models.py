from sqlalchemy import Boolean, Column, Integer, String

from atm_machines.database import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)
    completed = Column(Boolean, default=True)
