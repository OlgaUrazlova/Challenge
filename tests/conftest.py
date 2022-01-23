import allure
import pytest
from lib.requests import Requests


@pytest.fixture(scope="function")
def get_user_list():
    response = Requests.get("/users")
    data_in_response = response.json()["data"]

    return data_in_response[0]


@pytest.fixture(scope="function")
def get_deleted_user():
    test_data = {
        "name": "Deleted User",
        "job": "tester"
    }

    response = Requests.post("/user", data=test_data)
    user_id = response.json()["id"]

    response_delete = Requests.delete(f"/users/{user_id}")
    assert response_delete.status_code == 204

    return user_id

