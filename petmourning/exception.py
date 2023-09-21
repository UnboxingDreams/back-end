class CustomException(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status = status_code
        super().__init__(message)

class ExpiredException(Exception):
    def __init__(self, status_code=403):
        self.message = "this token is Expired. You should Login Again."
        self.status = status_code
        super().__init__(self.message)

class InvalidException(Exception):
    def __init__(self, status_code=401):
        self.message = "this token is Invalid. You should SignUp."
        self.status = status_code
        super().__init__(self.message)