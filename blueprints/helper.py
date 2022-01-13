from functools import wraps
from flask import request
from db_helpers.Group import Group
from exceptions.Unauthorized import Unauthorized
from db_helpers.User import User

def require_token():
    if not request.json.get("token") or not User.authenticate_token(request.json.get("token")):
        raise Unauthorized("Access token was not provided or is invalid", "Authentication")

def require_same_user_as_email(f):
    @wraps(f)
    def view(*args, **kwargs):
        require_token()
        if kwargs.get("email") != User.authenticate_token(request.json.get("token")).email:
            raise Unauthorized("Access token is invalid", "Authentication")
        return f(*args, **kwargs)
    return view

def require_same_user_as_group_id_user(f):
    """Verify that the user from the token is the owner of the group_id group"""
    @wraps(f)
    def view(*args, **kwargs):
        require_token()
        
        if kwargs.get("id") and Group.get_by_id(kwargs["id"]).user_id != User.authenticate_token(request.json.get("token")).id:
            raise Unauthorized("You do not own this group", "Authentication")
        return f(*args, **kwargs)
    return view