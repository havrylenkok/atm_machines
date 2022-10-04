from datetime import datetime

import pytest

from atm_machines.atms.controllers import AtmsController
from atm_machines.atms.schemas import AtmCreateParams
from atm_machines.tests import TEST_ENDPOINT, TEST_LAT, TEST_LONG


def test_atms__controller_create_atm__positive(atm_machines_db_session):
    # given
    params = AtmCreateParams(
        address="address", provider="provider", longitude=TEST_LONG, latitude=TEST_LAT
    )

    # when
    atm = AtmsController(atm_machines_db_session).create_atm(params)

    # then
    assert atm.geography is not None
    assert atm.address == params.address
    assert atm.provider == params.provider
    assert atm.created_at.date() == datetime.now().date()


@pytest.mark.parametrize(
    "params,expected_message",
    [
        ({"provider": "1"}, "field required"),
        ({"address": "1"}, "field required"),
        ({"provider": "1", "address": "1", "longitude": "q"}, "value is not a valid float"),
        ({"provider": "1", "address": "1", "latitude": "q"}, "value is not a valid float"),
    ],
)
def test_atms__view_create_atm__params_negative(test_client, params, expected_message):
    # given
    # when
    response = test_client.post(f"{TEST_ENDPOINT}", json=params)

    # then
    assert response.status_code == 422
    assert expected_message in response.text
