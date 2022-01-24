import json
import datetime

from requests import Response


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Response is not in JSON format. Response text is '{response.text}'")

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Response is not in JSON format. Response text is '{response.text}'")

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_keys_in_data(response: Response, names: list):
        try:
            response_as_dict = response.json()
            data_in_response = response_as_dict["data"]
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Response is not in JSON format. Response text is '{response.text}'")

        for name in names:
            assert name in data_in_response, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Response is not in JSON format. Response text is '{response.text}'")

        for name in names:
            assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_params_types_string(response: Response, names: list):
        try:
            response_as_dict = response.json()
            for name in names:
                isinstance(response_as_dict[name], str)
        except TypeError:
            raise TypeError("Incorrect value type")

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, f"Unexpected status code. Actual: {response.status_code}." \
                                                             f"Expected: {expected_status_code}"

    @staticmethod
    def assert_json_has_not_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Response is not in JSON format. Response text is '{response.text}'")

        for name in names:
            assert name not in response_as_dict, f"Response JSON shouldn't have key '{name}'"

    @staticmethod
    def assert_header_value_by_name(response: Response, name, expected_value, error_message):
        header = response.headers

        assert name in header, f"Response header doesn't have key '{name}'"
        assert header[name] == expected_value, error_message

    @staticmethod
    def assert_datetime_format_is_correct(response: Response, name):
        try:
            response_as_dict = response.json()
            datetime.datetime.strptime(response_as_dict[name], "%Y-%m-%dT%H:%M:%S.%fZ")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Response is not in JSON format. Response text is '{response.text}'")
        except ValueError:
            raise ValueError("Incorrect data format, should be like '2022-01-23T09:17:08.734Z'")

    @staticmethod
    def assert_basic_payload_params_status_code_header(response: Response, expected_status_code, names: list,
                                                       header_content_type):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Response is not in JSON format. Response text is '{response.text}'")

        assert response.status_code == expected_status_code, f"Unexpected status code. Actual: {response.status_code}." \
                                                             f"Expected: {expected_status_code}"
        for name in names:
            assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        assert response.headers["Content-Type"] == header_content_type

