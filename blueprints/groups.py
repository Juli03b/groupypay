"""Blueprint for users views"""

from functools import wraps
from flask import request
from flask.blueprints import Blueprint
from flask.json import jsonify
from blueprints.helper import require_same_user_as_email, require_token
from db_helpers.Group_Payment import Group_Payment
from db_helpers.Member_Payment import Member_Payment
from exceptions.Unauthorized import Unauthorized
from json_validation import validate_json
from db_helpers.User import User
from exceptions.Bad_Request import Bad_Request
from db_helpers.Group import Group
from db_helpers.Group_Member import Group_Member
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request

groups_blueprint = Blueprint("groups", __name__)

def users_blueprint(f):
    @wraps(f)
    def decorated_function2(*args, **kwargs):
        if not request.json.get("token") or not User.authenticate_token(request.json.get("token")):
            raise Unauthorized("Access token was not provided or is not credible")
        return f(*args, **kwargs)
    return decorated_function2
def require_same_id(f):
    @wraps(f)
    def decorated_function1(*args, **kwargs):
        if Group.get_by_id(12).user_id != User.authenticate_token(request.json.get("token")).id:
            raise Unauthorized("You do not own this group")
        return f(*args, **kwargs)
    return decorated_function1


# @require_same_user_as_email
@groups_blueprint.get("/", strict_slashes=False)
def get_groups(email: str):
    """Get groups"""
    user = User.get_by_email(email)

    return jsonify(user.groups), 200

@groups_blueprint.post("/", strict_slashes=False)
@require_same_user_as_email
def make_group(email: str):
    """Make a group"""
    validate_json(request.json, "group")
    
    user = User.get_by_email(email)
    group = user.make_group(request.json.get("name"), request.json.get("description"), request.json.get("secret_code"))
    
    return jsonify(group), 201

@groups_blueprint.get("/<id>")
@jwt_required(optional=True)
def get_group(email: str, id: str):
    """Get a group"""
    current_user = get_jwt_identity()
    user = User.get_by_email(email)
    group = user.get_group(id, current_user.get("email") if current_user else None, request.args.get("secret_code"))
    
    if not group:
        raise Bad_Request("Secret code is not correct")
    
    return jsonify(group)
    
# @require_token
@groups_blueprint.patch("/<id>")
@require_same_id
def patch_group(id: str):
    """Patch group"""
    if not request.json:
        raise Bad_Request("No name or description was provided")
    
    group = Group.get_by_id(id)
    group.edit(request.json.get("name"), request.json.get("description"))
    
    return jsonify(message="Changes were made successfully"), 200

#! /groups/<group_id>/members

@groups_blueprint.get("/<group_id>/members")
def get_members(group_id: int):
    """Get all members in group"""
    group = Group.get_by_id(group_id)
    return jsonify(members=group.members)

@groups_blueprint.get("/<group_id>/members/<member_id>")
def get_member(group_id: int, member_id: int):
    """Get member with member_id in group with group_id"""
    group_member = Group_Member.get_by_id(member_id, group_id)

    return jsonify(group_member.__dict__)

@groups_blueprint.post("/<group_id>/members")
@jwt_required(optional=True)
def add_member(email: str, group_id: int):
    validate_json(request.json, "group_member")
    current_user = get_jwt_identity()

    user = User.get_by_email(email)
    group = user.get_group(group_id, current_user.get("email"))
    member = group.add_member(request.json.get("name"), request.json.get("email"), request.json.get("phone_number"))
    
    return jsonify(message="Successfully created group member", member=member.__dict__), 201

# @require_token
@require_same_id
@groups_blueprint.patch("/<group_id>/members/<member_id>")
def patch_group_member(group_id: int, member_id: int):
    validate_json(request.json, "user_patch")

    group_member = Group_Member.get_by_id(member_id, group_id)
    group_member.edit(request.json["name"], request.json["email"], request.json["phone_number"])
    
    return jsonify(message="Changes were made successfully", group_member=group_member), 200

#! /groups/<group_id>/payments

@groups_blueprint.get("/<group_id>/payments")
def get_group_payments(group_id: int):
    group = Group.get_by_id(group_id)
    
    return jsonify(group_payments=group.payments)

@groups_blueprint.get("/<group_id>/payments/<payment_id>")
def get_group_payment(group_id: int, payment_id: int):
    group_payment = Group_Payment.get_by_id(payment_id, group_id)
    group_payment.total_amount = str(group_payment.total_amount)
    return jsonify(group_payment)

@groups_blueprint.post("/<group_id>/payments")
@jwt_required(optional=True)
def add_group_payment(email, group_id: int):
    """Add group payment"""
    if not request.json or not request.json.get("name") or not  request.json.get("total_amount"):
        raise Bad_Request("Missing information")
    current_user = get_jwt_identity()
    user = User.get_by_email(email)
    group = user.get_group(group_id, current_user.get("email"))
    group_payment = group.add_payment(request.json["name"], request.json["total_amount"], request.json["member_id"])
    
    group_payment.add_member_payments(request.json["member_payments"])
    group_payment.total_amount = str(group_payment.total_amount)
    
    return jsonify(group_payment)

# @require_token
@require_same_id
@groups_blueprint.patch("/<group_id>/payments/<payment_id>")
def patch_group_payment(group_id: int, payment_id: int):
    if not request.json:
        raise Bad_Request("Missing information")

    group_payment = Group_Payment.get_by_id(payment_id, group_id)
    group_payment.edit(request.json.get("name"), request.json.get("total_amount"))
    
    return jsonify(message="Changes were made successfully", group_payment=group_payment), 200

# @require_same_id
@groups_blueprint.post("/<group_id>/payments/<payment_id>")
def create_member_payments(group_id: int, payment_id: int):
    """Craete Member Payments (member payment list from json body)"""
    if not request.json:
        raise Bad_Request("Missing information")

    group_payment = Group_Payment.get_by_id(payment_id, group_id)

    return jsonify(message="Changes were made successfully", group_payment=group_payment), 200

#! /groups/<group_id>/payments/<group_payment_id>/member_payments

@groups_blueprint.get("/<group_id>/payments/<group_payment_id>")
def get_member_payments(group_id: int, group_payment_id: int):
    """Get a group payment's member payments"""
    group_payment = Group_Payment.get_by_id(group_payment_id, group_id)
    
    return jsonify(member_payments=group_payment.member_payments)

#! /groups/<group_id>/payments/<group_payment_id>/member_payments/members/<member_id>

@groups_blueprint.get("/<group_id>/payments/<group_payment_id>/member_payments/members/<member_id>")
def get_member_payment(group_payment_id: int, member_id):
    member_payment = Member_Payment.get_by_id(member_id, group_payment_id)
    
    return jsonify(member_payment=member_payment)

@groups_blueprint.post("/<group_id>/payments/<group_payment_id>/member_payments/members/<member_id>")
def make_member_payment(group_payment_id: int, member_id):
    member_payment = Member_Payment.get_by_id(member_id, group_payment_id)
    
    return jsonify(member_payment=member_payment)

@groups_blueprint.post("/<group_id>/payments/<group_payment_id>/member-payments/<member_id>/pay", strict_slashes=False)
@jwt_required(optional=True)
def pay_payment(email, group_id, group_payment_id: int, member_id):
    """Pay processes"""
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", email, group_id, group_payment_id, member_id, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    user = User.get_by_email(email)
    current_user = get_jwt_identity()

    group = user.get_group(group_id, current_user.get("email"))
    payment = group.get_payment(group_payment_id)
    
    member_payment = payment.get_member_payment(member_id)
    member_payment.pay()
    
    return jsonify("Paid"), 200