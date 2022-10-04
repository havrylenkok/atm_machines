from datetime import datetime
from urllib.parse import urlencode

import pytest

from atm_machines.atms.controllers import AtmsController
from atm_machines.atms.models import AtmModel
from atm_machines.atms.schemas import AtmsReadParams
from atm_machines.tests import TEST_ENDPOINT, TEST_GEOGRAPHY, TEST_LAT, TEST_LONG


def test_atms__controller_read_atms__positive(atm_machines_db_session):
    # given
    atm = AtmModel(address="address", provider="provider", geography=TEST_GEOGRAPHY)
    atm_machines_db_session.add(atm)
    atm_machines_db_session.commit()
    atm_machines_db_session.refresh(atm)

    params = AtmsReadParams()

    # when
    rows = AtmsController(atm_machines_db_session).read_atms(params)

    # then
    res_atm = rows[0]

    assert res_atm["created_at"].date() == datetime.now().date()
    assert res_atm["address"] == atm.address
    assert res_atm["provider"] == atm.provider
    assert res_atm["longitude"] == TEST_LONG
    assert res_atm["latitude"] == TEST_LAT


@pytest.mark.parametrize(
    "limit,offset",
    [
        (0, 0),
        (1, 0),
        (0, 1),
    ],
)
def test_atms__controller_read_atms__limit_offset(atm_machines_db_session, limit, offset):
    # given
    unique_atm = AtmModel(address="unique", provider="provider", geography=TEST_GEOGRAPHY)
    atms = [AtmModel(address="address", provider="provider", geography=TEST_GEOGRAPHY)] * 5
    atm_machines_db_session.add(unique_atm)
    atm_machines_db_session.add_all(atms)
    atm_machines_db_session.commit()
    atm_machines_db_session.refresh(unique_atm)

    params = AtmsReadParams(limit=limit, offset=offset)

    # when
    rows = AtmsController(atm_machines_db_session).read_atms(params)

    # then
    assert len(rows) == limit
    if not limit:
        return

    if offset:
        assert rows[0]["id"] != unique_atm.id


@pytest.mark.parametrize(
    "longitude,latitude,expect_match",
    [
        (TEST_LONG, TEST_LAT, True),
        (5.0, 5.0, False),
        (5.0, None, True),
        (None, 5.0, True),
    ],
)
def test_atms__controller_read_atms__point(
    atm_machines_db_session, longitude, latitude, expect_match
):
    # given
    atm = AtmModel(address="unique", provider="provider", geography=TEST_GEOGRAPHY)
    atm_machines_db_session.add(atm)
    atm_machines_db_session.commit()
    atm_machines_db_session.refresh(atm)

    params = AtmsReadParams(longitude=longitude, latitude=latitude)

    # when
    rows = AtmsController(atm_machines_db_session).read_atms(params)

    # then
    if expect_match:
        assert rows[0]["id"] == atm.id
        if longitude and latitude:
            assert rows[0]["distance"] is not None
        else:
            assert "distance" not in rows[0]
    else:
        assert not rows


def test_atms__controller_read_atms__radius():
    # todo: cut corner
    # check that query is filtered by radius when point is present
    pass


def test_atms__view_read_atms__params_positive(monkeypatch, test_client):
    # given
    params = dict(limit=2)

    def mocked_read_atms(*args, **kwargs):
        nonlocal params

        # then
        assert kwargs["params"].limit == params["limit"]
        return []

    monkeypatch.setattr(AtmsController, "read_atms", mocked_read_atms)

    # when
    response = test_client.get(f"{TEST_ENDPOINT}?{urlencode(params)}")

    # then
    assert response.status_code == 200
    data = response.json()
    assert data == []


@pytest.mark.parametrize(
    "params,expected_message",
    [
        ({"limit": -1}, "ensure this value is greater than or equal to 0"),
        ({"radius": -1}, "ensure this value is greater than or equal to 0"),
        ({"radius": 2001}, "ensure this value is less than or equal to 2000"),
        ({"offset": -1}, "ensure this value is greater than or equal to 0"),
    ],
)
def test_atms__view_read_atms__params_negative(test_client, params, expected_message):
    # given
    # when
    response = test_client.get(f"{TEST_ENDPOINT}?{urlencode(params)}")

    # then
    assert response.status_code == 422
    assert expected_message in response.text
