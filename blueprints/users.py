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
def get_user(id):
    """Get users view. Get user information, admin only"""
    
    user = User.get_user_by_id(id)
    
    return jsonify(user)