"""Module for Bad_Request exception"""

from .Custom_Error import Custom_Error

class Bad_Request(Custom_Error):
    """Exception to use when there's a client error, 400"""

    def __init__(self, message:str, cause:str=None, **kwargs):
        super().__init__(message, cause, 400, **kwargs)

    def __repr__(self):
        return super().__repr__(self)
        