class ErrorResponse:
    HTTP_401_UNAUTHORIZED = {
        401: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid token"
                    }
                }
            },
        }
    }

    HTTP_401_INVALID_LOGIN_OR_PASSWORD = {
        401: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid login or password"
                    }
                }
            },
        }
    }

    HTTP_401_INVALID_LOGIN = {
        401: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid login"
                    }
                }
            },
        }
    }