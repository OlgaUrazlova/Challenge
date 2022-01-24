import allure
import pytest

from lib.helpers import Helpers
from lib.my_requests import MyRequests
from lib.assertion import Assertions


@allure.epic("These tests check technical validation")
class TestBaseCases:
    @allure.title("Test check sending data using wrong method")
    @pytest.mark.parametrize("method_name", ["get", "put", "delete"])
    @pytest.mark.xfail(reason="In this dummy service there is no method validation")
    def test_user_creating_with_wrong_method(self, method_name):
        assert Helpers.method_validation(method_name) == 405

    @allure.title("Test check sending data using wrong method")
    @pytest.mark.parametrize("method_name", ["post", "put", "delete"])
    @pytest.mark.xfail(reason="In this dummy service there is no method validation")
    def test_getting_user_info_with_wrong_method(self, method_name):
        assert Helpers.method_validation(method_name) == 405

    @allure.title("Test check sending request with wrong content-type")
    def test_user_creating_with_wrong_content_type(self):
        test_data = {
            "name": "Tester Name",
            "job": "testing"
        }

        response = MyRequests.post("/user", data=test_data, headers={"Content-Type": "text/plain"})

        Assertions.assert_basic_payload_params_status_code_header(response, 201, ["id", "createdAt"],
                                                                  "application/json; charset=utf-8")

    @allure.title("Test check sending user creating request to the wrong URL")
    def test_user_creating_with_wrong_url(self):
        response_post = MyRequests.post("")

        Assertions.assert_code_status(response_post, 404)

    @allure.title("Test check sending request to get info about user to the wrong URL")
    def test_getting_user_info_from_wrong_url(self):
        response_get = MyRequests.get("")

        Assertions.assert_code_status(response_get, 404)




