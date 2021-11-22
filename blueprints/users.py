"Blueprint for users views"

from flask_jwt_extended import create_access_token
from flask import request
from flask.blueprints import Blueprint
from flask.json import jsonify
from email_validator import EmailNotValidError, validate_email
from json_validation import validate_json
from phone_number_validation import validate_phone_number
from db_helpers.User import User
from exceptions.BadRequest import BadRequest

users_blueprint = Blueprint("users", __name__)

@users_blueprint.post("/", strict_slashes=False)
def sign_up():
    """Sign up view. Validate json request body and create user if valid"""

    # Check if JSON request is valid, return error and HTTP code accordingly
    validate_json(request.json, "user_schema")

    # Parse and validate phone number if exists
    if phone_number := request.json.get("phone_number"):
        formated_number = validate_phone_number(phone_number)
        request.json["phone_number"] = formated_number

    try:
        validate_email(request.json.get("email"))
    except EmailNotValidError as error:
        raise BadRequest(message=str(error), cause="email") from error

    user = User.sign_up(**request.json)
    access_token = create_access_token(user.email)
    warning = dict(message="Phone number was not provided, none saved", cause="phone_number")

    return jsonify(
        message="Sign up successful",
        warning=warning if not request.json.get("phone_number") else None,
        access_token=access_token), 201

@users_blueprint.get("/<id>", strict_slashes=False)
def get_user(id):
    """Get users view. Get user information, admin only"""
    
    user = User.get_user_by_id(id)
    
    return jsonify(user)