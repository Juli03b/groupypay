"Blueprint for users views"

from flask_jwt_extended import create_access_token
from flask import request
from flask.blueprints import Blueprint
from flask.json import jsonify
from json_validation import validate_json
from phone_number_validation import validate_phone_number
from email_validator import EmailNotValidError, validate_email
from db_helpers.User import User
from exceptions.BadRequest import BadRequest
users_blueprint = Blueprint("users", __name__)

@users_blueprint.post("/", strict_slashes=False)
def sign_up():
    try:
        # Check if JSON request is valid, return error and HTTP code accordingly
        validate_json(request.json, "user_schema")

        # Parse and validate phone number if exists
        if phone_number := request.json.get("phone_number"):
            formated_number = validate_phone_number(phone_number)
            request.json["phone_number"] = formated_number

        try:
            validate_email(request.json.get("email"))
        except EmailNotValidError as e:
            raise BadRequest(message=str(e), cause="email")
        
        user = User.sign_up(**request.json)
        access_token = create_access_token(user.email)

        return jsonify(
            message="Sign up successful", 
            warning=dict(message="Phone number was not provided, none saved", cause="phone_number") if not request.json.get("phone_number") else None, 
            access_token=access_token), 201

    except BadRequest as e:
        error, status_code = e.formated
        return jsonify(error), status_code