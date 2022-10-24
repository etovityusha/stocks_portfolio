from unittest.mock import patch

from starlette.testclient import TestClient

from repo.currency import CurrencyObj


@patch("api.currencies.views.CurrencyRepo.find")
def test_currencies_listing(find, test_client: TestClient) -> None:
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


@patch("api.currencies.views.CurrencyRepo.get_by_id")
def test_currency_details(get_by_id, test_client: TestClient) -> None:
    get_by_id.return_value = CurrencyObj(id=3, code="TEST_CODE3", name="TEST_NAME3")
    response = test_client.get("/currencies/3")
    assert response.status_code == 200
    assert response.json() == {"code": "TEST_CODE3", "id": 3, "name": "TEST_NAME3"}


@patch("api.currencies.views.CurrencyRepo.create_new")
def test_post_new_currency(create_new, test_client: TestClient) -> None:
    create_new.return_value = CurrencyObj(id=3, code="TEST_CODE3", name="TEST_NAME3")
    response = test_client.post(
        "/currencies", json=dict(code="TEST_CODE3", name="TEST_NAME3")
    )
    assert response.json() == {"id": 3}
    assert response.status_code == 201
