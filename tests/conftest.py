import pytest
from lib.my_requests import MyRequests


@pytest.fixture
def get_user_list():
    response = MyRequests.get("/users")
    data_in_response = response.json()["data"]

    return data_in_response[0]


@pytest.fixture
def get_deleted_user():
    test_data = {
        "name": "Deleted User",
        "job": "tester"
    }

    response = MyRequests.post("/user", data=test_data)
    user_id = response.json()["id"]

    response_delete = MyRequests.delete(f"/users/{user_id}")
    assert response_delete.status_code == 204

    return user_id


@pytest.fixture
def create_new_user():
    test_data = {
        "name": "New User 1",
        "job": "tester 1"
    }

    response_1 = MyRequests.post("/user", data=test_data)
    response_2 = MyRequests.post("/user", data=test_data)
    user_id_1 = response_1.json()["id"]
    user_id_2 = response_2.json()["id"]
    users_ids = [user_id_1, user_id_2]

    return users_ids


@pytest.fixture
def create_new_user_with_long_name():
    name = "N" * 256
    job = "J" * 256

    test_data = {
        "name": name,
        "job": job
    }

    return test_data
