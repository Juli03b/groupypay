"""Module for Unauthorized exception"""

from .Custom_Error import Custom_Error

class Unauthorized(Custom_Error):
    """Client invalid authentication credentials, 401"""

    def __init__(self, message: str, cause: str, **kwargs):
        super().__init__(message, cause, 401, **kwargs)

    def __repr__(self):
        return super().__repr__(self)
        