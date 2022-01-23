import allure
import pytest
from lib.assertion import Assertions
from lib.requests import Requests


@allure.epic("New user creating")
@allure.testcase(
    "https://docs.google.com/spreadsheets/d/1G0GwfdGZFxHw7pk2FUmShdH91QXZsEse65-bbTDL0GQ/edit#gid=1850653866",
    "Test cases to check user creating")
class TestUserCreate:
    """As these tests are created for the dummy service, which doesn't have any validation, I have to use my
    previous experience and assume some validation errors"""

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Positive test: successful new user creating and getting info about it")
    @pytest.mark.xfail(reason="This test is an expected failure")
    def test_new_user_creating(self):
        """This test is an expected failure, cause this dummy service doesn't save any new users, so it's impossible to
        get info about them. Further I don't use GET request for the same reason"""
        test_data = {
            "name": "Test User",
            "job": "tester"
        }

        response = Requests.post("/user", data=test_data)

        Assertions.assert_code_status(response, 201)
        Assertions.assert_json_has_keys(response, ["name", "job", "id", "createdAt"])
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
        Assertions.assert_header_value_by_name(
            response,
            "Content-Type",
            "application/json; charset=utf-8",
            "Content-Type of the response is different from the expected"
        )

        get_response = Requests.get(f"/users/{response.json()['id']}")

        Assertions.assert_code_status(get_response, 200)
        Assertions.assert_json_has_keys_in_data(response, ["id", "email", "first_name", "last_name", "avatar"])

    @allure.description("Positive test: successful user creating with the same data")
    def test_users_creating_with_the_same_values(self):
        """In this dummy service new user is always created, cause there's no fields validation"""
        test_data = {
            "name": "Test Tester",
            "job": "PM"
        }

        ids = []

        for i in range(2):
            response = Requests.post("/user", data=test_data)
            Assertions.assert_code_status(response, 201)
            ids += response.json()["id"]

        assert ids[0] != ids[1], f"Expected two new users, but in the response ids are the same {ids[0]} and {ids[1]}"

    @allure.description("Positive test: successful user creating without optional values")
    @pytest.mark.parametrize("name", ["", None])
    @pytest.mark.parametrize("job", ["", None])
    def test_user_creating_without_optional_values(self, name, job):
        """I checked the behaviour of the service and suppose that all parameters are optional"""
        test_data = {
            "name": name,
            "job": job
        }

        response = Requests.post("/user", data=test_data)

        Assertions.assert_code_status(response, 201)
        Assertions.assert_json_has_keys(response, ["id", "createdAt"])
        if test_data["name"] == "":
            Assertions.assert_json_has_key(response, "name")
        elif test_data["job"] == "":
            Assertions.assert_json_has_key(response, "job")
        else:
            Assertions.assert_json_has_not_key(response, "name")
            Assertions.assert_json_has_not_key(response, "job")

    @allure.description("Positive test: successful user creating without payload")
    def test_user_creating_without_payload(self):
        response = Requests.post("/user")

        Assertions.assert_code_status(response, 201)
        Assertions.assert_json_has_keys(response, ["id", "createdAt"])
        Assertions.assert_json_has_not_key(response, "name")
        Assertions.assert_json_has_not_key(response, "job")

    # Test data to check if it's possible to save in DB a string value longer than 255 symbols
    long_name = "T" * 256
    long_job = "T" * 256

    @allure.description("Positive test: values length is more than 255 symbols")
    @pytest.mark.parametrize(
        "name,job,expected",
        [
            pytest.param(
                long_name, "QA", "name", id="name is too long"
            ),
            pytest.param(
                "New User", long_job, "job", id="job is too long"
            ),
        ],
    )
    def test_user_creating_with_too_long_values(self, name, job, expected):
        """This test checks if it's possible to insert string in DB longer than 255 symbols"""
        test_data = {
            "name": name,
            "job": job
        }

        response = Requests.post("/user", data=test_data)
        name_from_request = response.json()["name"]
        job_from_request = response.json()["job"]

        Assertions.assert_code_status(response, 201)

        if expected == "name":
            assert len(name_from_request) == len(name), "Name length from the response is not the same as the request"
        elif expected == "job":
            assert len(job_from_request) == len(job), "Job length from the response is not the same as the request"

    @allure.description("Positive test: values contain special symbols and Cyrillic alphabet")
    @pytest.mark.parametrize(
        "name,job",
        [
            pytest.param(
                "!@=+-*(^&%$>", "тестировщик", id="Name is special symbols and job is Cyrillic"
            ),
            pytest.param(
                "Тест Тестович Тестов", "!@=+-*(^&%$>",
                id="Name is Cyrillic symbols and job is special symbols"
            ),
        ],
    )
    def test_user_creating_with_special_and_cyrillic_symbols(self, name, job):
        test_data = {
            "name": name,
            "job": job

        }

        response = Requests.post("/user", data=test_data)

        Assertions.assert_code_status(response, 201)
        Assertions.assert_json_has_keys(response, ["name", "job", "id", "createdAt"])
        Assertions.assert_params_types_string(response, ["name", "job", "id", "createdAt"])
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

    @allure.description("Negative test: wrong types of values in payload")
    @pytest.mark.parametrize(
        "name,job,expected",
        [
            pytest.param(
                123, "QA", "name", id="name is int"
            ),
            pytest.param(
                "New User", 123, "job", id="job is int"
            ),
            pytest.param(
                ["Test1", "Test2"], "QA", "name", id="name is list"
            ),
            pytest.param(
                "New User", ["QA", "Tester"], "job", id="job is list"
            )
        ],
    )
    @pytest.mark.xfail(reason="This test is an expected failure cause there is no types validation")
    def test_user_creating_with_incorrect_types_of_values(self, name, job, expected):
        """This test is negative, according to the schema from the service description all parameters
        should be strings"""
        test_data = {
            "name": name,
            "job": job
        }

        response = Requests.post("/user", data=test_data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_has_not_key(response, "id")
        Assertions.assert_json_value_by_name(
            response,
            "message",
            f"The type of the {expected} attribute must be 'string'.",
            "Actual error message is different from the expected"
        )

    @allure.description("Negative test: incorrect names of the parameters")
    @pytest.mark.xfail(reason="There isn't validation of the parameters names in this dummy service")
    def test_user_creating_with_invalid_fields(self):
        """This test checks that incorrect fields name should be interpreter like blank values and shouldn't be saved"""
        test_data = {
            "names": "New User",
            "jobs": "QC"
        }

        response = Requests.post("/user", data=test_data)

        Assertions.assert_code_status(response, 201)
        Assertions.assert_json_has_keys(response, ["id", "createdAt"])
        Assertions.assert_json_has_not_key(response, "name")
        Assertions.assert_json_has_not_key(response, "job")




