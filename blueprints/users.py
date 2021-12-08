"""Blueprint for users views"""

from flask_jwt_extended import create_access_token
from flask import request
from flask.blueprints import Blueprint
from flask.json import jsonify
from email_validator import EmailNotValidError, validate_email
from json_validation import validate_json
from phone_number_validation import validate_phone_number
from db_helpers.User import User
from exceptions.Bad_Request import Bad_Request

users_blueprint = Blueprint("users", __name__)

@users_blueprint.get("/<id>", strict_slashes=False)
def get_user(id: int):
    """Get users view. Get user information."""
    
    user = User.get_by_id(id)
    return jsonify(user.__dict__)

@users_blueprint.patch("/<id>", strict_slashes=False)
def patch_user(id: int):
    """Patch user"""
    
    user = User.get_by_id(id)
    
    # Validate json
    validate_json(request.json, "user_patch")
    
    # Validate email
    if request.json.get("email"):
        try:
            validate_email(request.json["email"])
        except EmailNotValidError as error:
            raise Bad_Request(message=str(error), cause="email") from error
    user.edit(request.json.get("name"), request.json.get("email"), request.json.get("phone_number"), request.json.get("password"))
    
    return jsonify(message="Changes were made succesfully"), 200

@users_blueprint.post("/<id>/groups", strict_slashes=False)
def make_group(id):
    """Make a group"""
    
    user = User.get_by_id(id)
    user.make_group(request.json.get("name"), request.json.get("description"))
    
    return jsonify(message="Group was created succesfully"), 201