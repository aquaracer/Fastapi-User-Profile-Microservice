class TokenExpiredError(Exception):
    detail = "Token has expired"


class TokenIsNotCorrectError(Exception):
    detail = "Token is not correct"


class UserProfileExistsError(Exception):
    def __init__(self, user_id: int):
        self.detail = f"User Profile yet created for user_id: {user_id}"


class UserProfileNotFoundError(Exception):
    def __init__(self, user_id: int):
        self.detail = f"UserProfile not found for user_id: {user_id}"
