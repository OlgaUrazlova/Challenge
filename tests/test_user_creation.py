import allure
import pytest
import simplejson as simplejson

from lib.assertion import Assertions
from lib.my_requests import MyRequests


@allure.epic("New user creating")
@allure.testcase(
    "https://docs.google.com/spreadsheets/d/1G0GwfdGZFxHw7pk2FUmShdH91QXZsEse65-bbTDL0GQ/edit#gid=1850653866",
    "Test cases to check user creating")
class TestUserCreate:
    """As these tests are created for the dummy service, which doesn't have any validation, I have to use my
    previous experience and assume some validation errors"""

    @allure.title("Positive test: successful new user creating and getting info about it")
    #@pytest.mark.xfail(reason="This test is an expected failure")
    def test_new_user_creating(self):
        """This test is an expected failure, cause this dummy service doesn't save any new users, so it's impossible to
        get info about them. Further I don't use GET request for the same reason"""
        test_data = {
            "name": "Test User",
            "job": "QA"
        }

        response = MyRequests.post("/user", data=test_data)

        Assertions.assert_basic_payload_params_status_code_header(response, 201, ["name", "job", "id", "createdAt"],
                                                                  "application/json; charset=utf-8")
        Assertions.assert_params_types_string(response, ["name", "job", "id", "createdAt"])
        Assertions.assert_datetime_format_is_correct(response, "createdAt")
        Assertions.assert_json_value_by_name(
            response,
            "name",
            test_data["name"],
            "User's name from request doesn't match user's name from response"
        )

        Assertions.assert_json_value_by_name(
            response,
            "job",
            test_data["job"],
            "User's job from request doesn't match user's job from response"
        )

        get_response = MyRequests.get(f"/users/{response.json()['id']}")

        Assertions.assert_code_status(get_response, 200)
        Assertions.assert_json_has_keys_in_data(response, ["id", "email", "first_name", "last_name", "avatar"])

    @allure.title("Positive test: successful user creating with the same data")
    def test_users_creating_with_the_same_values(self, create_new_user):
        """In this dummy service new user is always created, cause there's no fields validation"""
        assert create_new_user[0] != create_new_user[1], f"New user id '{create_new_user[1]}' is equal to the previous" \
                                                         f"user '{create_new_user[0]}'"

    @allure.title("Positive test: successful user creating without optional values")
    @pytest.mark.parametrize("name", ["", None])
    @pytest.mark.parametrize("job", ["", None])
    def test_user_creating_without_optional_values(self, name, job):
        """I checked the behaviour of the service and suppose that all parameters are optional"""
        test_data = {
            "name": name,
            "job": job
        }

        response = MyRequests.post("/user", data=simplejson.dumps(test_data))

        Assertions.assert_json_has_not_keys(response, ["name", "job"])

    @allure.title("Positive test: successful user creating without payload")
    def test_user_creating_without_payload(self):
        response = MyRequests.post("/user")

        Assertions.assert_json_has_not_keys(response, ["name", "job"])

    @allure.title("Positive test: values length is more than 255 symbols")
    def test_user_creating_with_too_long_values(self, create_new_user_with_long_name):
        """This test checks if it's possible to insert string in DB longer than 255 symbols"""
        response = MyRequests.post("/user", data=create_new_user_with_long_name)
        name_from_response = response.json()["name"]
        job_from_response = response.json()["job"]

        assert len(name_from_response) == 256, "Name length from the response is not the same as the request"
        assert len(job_from_response) == 256, "Name length from the response is not the same as the request"

    @allure.title("Positive test: values contain special symbols and Cyrillic alphabet")
    @pytest.mark.parametrize(
        "name,job", [("!@=+-*(^&%$>", "тестировщик"), ("Тест Тестович Тестов", "!@=+-*(^&%$>")],
        ids=["Name is special symbols and job is Cyrillic", "Name is Cyrillic symbols and job is special symbols"])
    def test_user_creating_with_special_and_cyrillic_symbols(self, name, job):
        test_data = {
            "name": name,
            "job": job
        }

        response = MyRequests.post("/user", data=test_data)

        Assertions.assert_json_value_by_name(
            response,
            "name",
            name,
            f"Name from response '{response.json()['name']}' differs from the request '{name}'"
        )
        Assertions.assert_json_value_by_name(
            response,
            "job",
            job,
            f"Value of job from response '{response.json()['job']}' differs from the request '{job}'"
        )

    @allure.title("Negative test: wrong types of values in payload")
    @pytest.mark.parametrize(
        "name,job,expected",
        [(123, "QA", "name"), ("New User", 123, "job"), (["Test1", "Test2"], "QA", "name"),
         ("New User", ["QA", "Tester"], "job")],
        ids=["name is int", "job is int", "name is list", "job is list"])
    @pytest.mark.xfail(reason="This test is an expected failure cause there is no types validation")
    def test_user_creating_with_incorrect_types_of_values(self, name, job, expected):
        """This test is negative, according to the schema from the service description all parameters
        should be strings"""
        test_data = {
            "name": name,
            "job": job
        }

        response = MyRequests.post("/user", data=test_data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(
            response,
            "message",
            f"The type of the {expected} attribute must be 'string'.",
            "Actual error message is different from the expected"
        )

    @allure.title("Negative test: incorrect names of the parameters")
    @pytest.mark.xfail(reason="There isn't validation of the parameters names in this dummy service")
    def test_user_creating_with_invalid_fields(self):
        """This test checks that incorrect fields name should be interpreter like blank values and shouldn't be saved"""
        test_data = {
            "names": "New User",
            "jobs": "QC"
        }

        response = MyRequests.post("/user", data=test_data)

        Assertions.assert_basic_payload_params_status_code_header(response, 201, ["id", "createdAt"],
                                                                  "application/json; charset=utf-8")
        Assertions.assert_json_has_not_keys(response, ["names", "jobs", "name", "job"])



