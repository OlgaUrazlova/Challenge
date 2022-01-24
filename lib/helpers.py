from lib.my_requests import MyRequests


class Helpers:
    @staticmethod
    def method_validation(method_name):
        if method_name == "get":
            response_get = MyRequests.get("/user")
            return response_get.status_code
        elif method_name == "post":
            response_get = MyRequests.post("/user")
            return response_get.status_code
        elif method_name == "put":
            response_get = MyRequests.put("/user")
            return response_get.status_code
        elif method_name == "delete":
            response_get = MyRequests.put("/user")
            return response_get.status_code




