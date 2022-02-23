"""Blueprint for users views"""

from flask import request
from flask.blueprints import Blueprint
from flask.json import jsonify
from email_validator import EmailNotValidError, validate_email
from blueprints.helper import require_same_user_as_email
from json_validation import validate_json
from db_helpers.User import User
from exceptions.Bad_Request import Bad_Request
from flask_jwt_extended import jwt_required

users_blueprint = Blueprint("users", __name__)

@users_blueprint.get("/<email>", strict_slashes=False)
def get_user(email: str):
    """Get user information"""
    user = User.get_by_email(email)
    return jsonify(user)

@users_blueprint.patch("/<email>", strict_slashes=False)
@require_same_user_as_email
def patch_user(email: str):
    """Patch user"""
    
    user = User.get_by_email(email)
    
    # Validate json
    validate_json(request.json, "user_patch")
    
    # Validate email
    if request.json.get("email"):
        try:
            validate_email(request.json["email"])
        except EmailNotValidError as error:
            raise Bad_Request(message=str(error), cause="email") from error
    user.edit(request.json.get("name"), request.json.get("email"), request.json.get("phone_number"), request.json.get("password"))
    del user.password
    return jsonify(user.__dict__), 200

@users_blueprint.get("/")
def search_users(name: str):
    """Search for users - name support only for now"""
    name = request.json.get("name")
    users = User.search_users(name)
    
    return jsonify(users)