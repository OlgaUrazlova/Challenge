import allure
import pytest
from lib.assertion import Assertions
from lib.requests import Requests


@allure.epic("New user creating")
@allure.testcase(
    "https://docs.google.com/spreadsheets/d/1G0GwfdGZFxHw7pk2FUmShdH91QXZsEse65-bbTDL0GQ/edit#gid=1850653866",
    "Test cases to check user creating")
class TestUserCreate():
    @allure.description("Successful new user creating and getting info about it")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_success_user_creating(self):
        test_data = {
            "name": "user",
            "job": "user job"
        }

        response = Requests.post("/api/user", data=test_data)

        Assertions.assert_code_status(response, 201)
        Assertions.assert_json_has_keys(response, ["name", "job", "id", "createdAt"])

        Assertions.assert_json_value_by_name(
            response,
            "name",
            test_data["name"],
            "User's name from request doesn't match user's name from response"
        )
