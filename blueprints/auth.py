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

@auth_blueprint.post("/token", strict_slashes=False)
def get_token():
    """Return token given username and password in request body"""
    
    # Check if JSON request is valid, return error and HTTP code accordingly
    validate_json(request.json, "auth")
    
    user = User.sign_in(request.json["email"], request.json["password"])
    
    del user.password

    return jsonify(token=create_access_token(user.__dict__, expires_delta=False))

@auth_blueprint.post("/sign-up", strict_slashes=False)
def sign_up():
    """Sign up view. Validate json request body and create user if valid"""

    # Check if JSON request is valid, return error and HTTP code accordingly
    valid_json = validate_json(request.json, "auth")
    
    # Parse and validate phone number if exists
    if phone_number := valid_json.get("phone_number"):
        formated_number = validate_phone_number(phone_number)
        valid_json["phone_number"] = formated_number

    try:
        validate_email(valid_json.get("email"))
    except EmailNotValidError as error:
        raise Bad_Request(message=str(error), cause="email") from error

    user = User.sign_up(**valid_json)
    access_token = create_access_token(user.__dict__, expires_delta=False)
    warning = "Phone number was not provided, none saved"

    return jsonify(
        message="Sign up successful",
        warning=warning if not valid_json.get("phone_number") else None,
        token=access_token), 201