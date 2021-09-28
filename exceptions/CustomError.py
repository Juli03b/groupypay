class CustomError(Exception):
    """Implement custom exceptions with this class"""

    def __init__(self, message: str, cause: str, status_code: int, **kwargs) -> None:
        self.message = message
        self.cause = cause
        self.status_code = status_code
        self.__dict__.update(kwargs)
        self.formated = dict(message=message, cause=cause, **kwargs), status_code
    def __repr__(cls, self):
        return f"<{cls} message={self.message} cause={self.cause}>"