from unittest.mock import patch

from starlette.testclient import TestClient

from repo.currency import CurrencyObj


@patch("api.currencies.views.CurrencyRepo.find")
def test_healthcheck(find, test_client: TestClient) -> None:
    find.return_value = [
        CurrencyObj(id=1, code="TEST_CODE1", name="TEST_TITLE1"),
        CurrencyObj(id=2, code="TEST_CODE2", name="TEST_TITLE2"),
    ]
    response = test_client.get("/currencies")
    assert response.status_code == 200
    assert response.json() == {
        "currencies": [
            {"code": "TEST_CODE1", "id": 1, "name": "TEST_TITLE1"},
            {"code": "TEST_CODE2", "id": 2, "name": "TEST_TITLE2"},
        ]
    }
