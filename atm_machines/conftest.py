import pytest
from main import app
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from atm_machines.database import Base, engine


@pytest.fixture(scope="session")
def atm_machines_tables():
    Base.metadata.create_all(engine)

    yield

    Base.metadata.drop_all(engine)


@pytest.fixture
def atm_machines_db_session(atm_machines_tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="package")
def test_client():
    return TestClient(app)
