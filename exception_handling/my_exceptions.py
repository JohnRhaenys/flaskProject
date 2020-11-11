class MyException(Exception):
    def __init__(self, message, response_json):
        self.message = message
        self.response_json = response_json
        super().__init__(self.message)


class NotEnoughParametersException(MyException):
    def __init__(self, message, response_json):
        super().__init__(message, response_json)


class InvalidParameterTypeException(MyException):
    def __init__(self, message, response_json):
        super().__init__(message, response_json)
