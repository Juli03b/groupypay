from flask_jwt_extended import create_access_token
from app import db
from models.Users import Users
from flask import request
from flask.blueprints import Blueprint
from flask.json import jsonify
from json_validation import validate_json
from sqlalchemy.exc import IntegrityError
from phone_number_validation import validate_phone_number
from email_validator import EmailNotValidError, validate_email
from db_helpers.User import User
users_blueprint = Blueprint("users", __name__)

@users_blueprint.post("/", strict_slashes=False)
def sign_up(): 
    valid_json, msg = validate_json(request.json, "user_schema")

    # Extra information to be returned, can be empty
    warning = None

    # Parse and validate phone number if exists. Set to false if parsing or validation fails
    if phone_number := request.json.get("phone_number"):
        formated_number, msg = validate_phone_number(phone_number)

        if formated_number:
            request.json["phone_number"] = formated_number
        else:
            warning = dict(message=msg, cause="phone_number")
    else:
        warning = dict(message="Phone number was not provided, none saved", cause="phone_number")

    # Check if JSON request is valid, return error and HTTP code accordingly
    if not valid_json:
        return jsonify(error=msg), 400

    try:
        validate_email(request.json["email"])
    except EmailNotValidError as e:
        return jsonify(error=dict(message=str(e), cause="email")), 400
    
    try:
        user = User.sign_up(**request.json)
    except Exception as e:
        return jsonify(e.args[0])
        
    access_token = create_access_token(user.email)

    return jsonify(message="Sign up successful", warning=warning, access_token=access_token), 201
