from CustomError import CustomError

class BadRequest(CustomError):
    def __init__(self, message:str, cause:str):
        super().__init__(message, cause, 400)

    def __repr__(cls, self):
        return super().__repr__(cls, self)