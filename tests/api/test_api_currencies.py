from unittest.mock import patch, MagicMock

from pydantic import BaseModel
from starlette.testclient import TestClient

from repo.currency import CurrencyObj


def test_currencies_listing(test_client: TestClient) -> None:
    response = test_client.get("/currencies")
    assert response.status_code == 200
    assert response.json() == {"currencies": []}


@patch("services.currency.CurrencyService.get_by_id")
def test_currency_details_success(get_by_id: MagicMock, test_client: TestClient) -> None:
    get_by_id.return_value = CurrencyObj(id=3, code="TEST_CODE3", name="TEST_NAME3")
    response = test_client.get("/currencies/3")
    assert response.status_code == 200
    assert response.json() == {"id": 3, "code": "TEST_CODE3", "name": "TEST_NAME3"}


def test_currency_details_404(test_client: TestClient) -> None:
    response = test_client.get("/currencies/3")
    assert response.status_code == 404
    assert response.json() == {"detail": "Currency not found"}


def test_post_new_currency(test_client: TestClient) -> None:
    response = test_client.post("/currencies", json=dict(code="TEST_CODE3", name="TEST_NAME3"))
    assert response.status_code == 201


@patch("services.currency.CurrencyService.update")
def test_update_currency(update: MagicMock, test_client: TestClient) -> None:
    class TestCase(BaseModel):
        service_response: int
        expected_status_code: int

    test_cases = [
        TestCase(service_response=1, expected_status_code=204),
        TestCase(service_response=10, expected_status_code=204),
        TestCase(service_response=0, expected_status_code=404),
    ]
    for case in test_cases:
        update.return_value = case.service_response
        response = test_client.patch("/currencies/1", json=dict(code="TEST_CODE", name="TEST_NAME"))
        assert response.status_code == case.expected_status_code
