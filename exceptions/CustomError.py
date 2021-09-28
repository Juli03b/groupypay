from typing import Tuple

from flask.json import jsonify

class CustomError(Exception):
    def __init__(self, message: str, cause: str, status_code: int) -> None:
        _message = message
        _cause = cause
        _status_code = status_code
        self.formated = dict(message=message, cause=cause), status_code
        self.json = jsonify(dict(message=message, cause=cause)), status_code

    def __repr__(cls, self):
        return f"<{cls} message={self.message} cause={self.cause}>"