import requests
import allure
from lib.logger import Logger


class Requests:
    @staticmethod
    def post(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"POST request to the URL '{url}'"):
            return Requests._send(url, data, headers, cookies, 'POST')

    @staticmethod
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"GET request to the URL '{url}'"):
            return Requests._send(url, data, headers, cookies, 'GET')

    @staticmethod
    def delete(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"DELETE request to the URL '{url}'"):
            return Requests._send(url, data, headers, cookies, 'DELETE')

    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str):

        url = f"https://reqres.in/api{url}"

        if headers is None:
            headers = {}
        elif cookies is None:
            cookies = {}

        Logger.add_request(url, data, headers, cookies, method)

        if method == "GET":
            response = requests.get(url, headers=headers, cookies=cookies, params=data)
        elif method == "POST":
            response = requests.post(url, headers=headers, cookies=cookies, data=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, cookies=cookies, data=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, cookies=cookies, data=data)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        Logger.add_response(response)

        return response
