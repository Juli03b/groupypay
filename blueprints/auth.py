"""Blueprint for auth views"""

from flask_jwt_extended import create_access_token
from flask import request
from flask.blueprints import Blueprint
from flask.json import jsonify
from email_validator import EmailNotValidError, validate_email
from json_validation import validate_json
from phone_number_validation import validate_phone_number
from db_helpers.User import User
from exceptions.Bad_Request import Bad_Request

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.post("/token", strict_slashes=True)
def get_token():
    """Return token given username and password in request body"""
    return request.json