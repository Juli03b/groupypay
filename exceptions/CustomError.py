"""Module for CustomError exception"""

class CustomError(Exception):
    """Implement custom exceptions with this class"""

    def __init__(self, message: str, cause: str, status_code: int, **kwargs) -> None:
        self.message = message
        self.cause = cause
        self.status_code = status_code
        self.__dict__.update(kwargs)
        self.formated = dict(message=message, cause=cause, **kwargs), status_code
        super().__init__(self.__dict__)

    def __repr__(self):
        return f"<{type(self)} message={self.message} cause={self.cause}>"
