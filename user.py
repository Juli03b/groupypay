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

users = Blueprint("users", __name__)

@users.post("/", strict_slashes=False)
def sign_up(): 
    valid_json, msg = validate_json(request.json, "user_schema")

    # Extra information to be returned, can be empty
    warning = None

    # Parse and validate phone number if exists, set to false if parsing or validation fails
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
        valid_email = validate_email(request.json["email"])
        print(valid_email.email)
    except EmailNotValidError as e:
        return jsonify(error=dict(message=str(e), cause="email")), 400
        
    # Create user
    user = Users.sign_up(**request.json)

    # Attempt making entry to db, return error and HTTP code if failed
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()

        [message] = e.orig.args

        return jsonify(error=dict(message=message, pg_code=e.orig.pgcode)), 409

    # Create jwt token containing user's email
    access_token = create_access_token(user.email)

    return jsonify(message="Sign up successful", warning=warning, access_token=access_token)
