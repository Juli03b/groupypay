from exceptions.CustomError import CustomError

class BadRequest(CustomError):
    """Exception to use when there's a client error, 400"""

    def __init__(self, message:str, cause:str, **kwargs):
        super().__init__(message, cause, 400, **kwargs)

    def __repr__(cls, self):
        return super().__repr__(cls, self)
        