from functools import wraps
from flask import request
from db_helpers.Group import Group
from exceptions.Unauthorized import Unauthorized
from db_helpers.User import User
from flask_jwt_extended import get_jwt_identity, jwt_required

def require_token():
    print("req token: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", dir(request), request.get_json)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!REQUIREDD!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if not request.json.get("token") or not User.authenticate_token(request.json.get("token")):
        return Unauthorized("Access token was not provided or is invalid", "Authentication")

def require_same_user_as_email(f):
    @wraps(f)
    @jwt_required()
    def view(*args, **kwargs):
        user = get_jwt_identity()
        if kwargs.get("email") != user["email"]:
            raise Unauthorized("Access token is invalid", "Authentication")
        return f(*args, **kwargs)
    return view

def require_same_user_as_group_id_user(f):
    """Verify that the user from the token is the owner of the group_id group"""
    @wraps(f)
    @jwt_required()

    def view(*args, **kwargs):        
        if kwargs.get("id") and Group.get_by_id(kwargs["id"]).user_id != User.authenticate_token(request.json.get("token")).id:
            raise Unauthorized("You do not own this group", "Authentication")
        return f(*args, **kwargs)
    return view