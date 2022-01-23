import allure
import pytest
from lib.assertion import Assertions
from lib.requests import Requests


@allure.epic("Getting info about a user")
@allure.testcase(
    "https://docs.google.com/spreadsheets/d/1G0GwfdGZFxHw7pk2FUmShdH91QXZsEse65-bbTDL0GQ/edit#gid=1332729984",
    "Test cases to check getting info about a user")
class TestGettingUserInfo:
    """As these tests are created for the dummy service, which doesn't have any validation and doesn't save any new user,
    I have to use my previous experience and assume some validation errors, and I also decided not to create new user
    and use already existing users in dummy service"""

    @allure.description("Positive test: get info about existing user")
    def test_getting_info_about_exciting_user(self, get_user_list):
        """This test use user id, which is reserved in this service"""
        response = Requests.get(f"/users/{get_user_list['id']}")

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_keys(response, ["data", "support"])
        assert response.json()["data"] == get_user_list, \
            f"Info about user from response {get_user_list} is differ from request"
        Assertions.assert_header_value_by_name(
            response,
            "Content-Type",
            "application/json; charset=utf-8",
            "Content-Type of the response is different from the expected"
        )

    @allure.description("Negative test: get info about deleted user")
    def test_getting_info_about_deleted_user(self, get_deleted_user):
        response = Requests.get(f"/users/{get_deleted_user}")

        Assertions.assert_code_status(response, 404)

    @allure.description("Negative test: get info about not existing user")
    def test_getting_info_about_not_exist_user(self):
        """Ids start counting from 1, so I suppose to use '0'"""
        response = Requests.get(f"/users/0")

        Assertions.assert_code_status(response, 404)






