"""Blueprint for users views"""

from flask_jwt_extended import create_access_token
from flask import request
from flask.blueprints import Blueprint
from flask.json import jsonify
from email_validator import EmailNotValidError, validate_email
from db_helpers.Group_Payment import Group_Payment
from db_helpers.Member_Payment import Member_Payment
from json_validation import validate_json
from phone_number_validation import validate_phone_number
from db_helpers.User import User
from exceptions.Bad_Request import Bad_Request
from db_helpers.Group import Group
from db_helpers.Group_Member import Group_Member

groups_blueprint = Blueprint("groups", __name__)

@groups_blueprint.get("/<id>")
def get_group(id: str):
    return jsonify(dict(Group.get_by_id(id)))

@groups_blueprint.patch("/<id>")
def patch_group(id: str):
    if not request.json:
        raise Bad_Request("No name or description was provided")
    
    group = Group.get_by_id(id)
    group.edit(request.json.get("name"), request.json.get("description"))
    
    return jsonify(message="Changes were made successfully"), 200

#! /groups/<group_id>/members

@groups_blueprint.get("/<group_id>/members")
def get_members(id: int):
    """Get all members in group"""
    group = Group.get_by_id(id)
    return jsonify(members=group.members)

@groups_blueprint.get("/<group_id>/members/<member_id>")
def get_member(group_id: int, member_id: int):
    """Get member with member_id in group with group_id"""
    group_member = Group_Member.get_by_id(member_id, group_id)

    return jsonify(group_member.__dict__)

@groups_blueprint.post("/<group_id>/members")
def add_member(group_id: int):
    validate_json(request.json, "user_patch")
    
    group = Group.get_by_id(group_id)
    member = group.add_member(request.json.get("name"), request.json.get("email"), request.json.get("phone_number"))
    
    return jsonify(message="Successfully created group member", member=member.__dict__), 201

@groups_blueprint.patch("/<group_id>/members/<member_id>")
def patch_group_member(group_id: int, member_id: int):
    validate_json(request.json, "user_patch")

    group_member = Group_Member.get_by_id(member_id, group_id)
    group_member.edit(request.json["name"], request.json["email"], request.json["phone_number"])
    
    return jsonify(message="Changes were made successfully", group_member=group_member), 200

#! /groups/<group_id>/payments

@groups_blueprint.get("/groups/<group_id>/payments")
def get_group_payments(group_id: int):
    group = Group.get_by_id(group_id)
    
    return jsonify(group_payments=group.payments)

@groups_blueprint.get("/groups/<group_id>/payments/<payment_id>")
def get_group_payment(group_id: int, payment_id: int):
    group_payment = Group_Payment.get_by_id(payment_id, group_id)
    
    return jsonify(group_payment=group_payment)

@groups_blueprint.post("/groups/<group_id>/payments")
def add_group_payment(group_id: int):
    if not request.json or not request.json.get("name") or not  request.json.get("total_amount"):
        raise Bad_Request("Missing information")
    
    group = Group.get_by_id(group_id)
    group_payment = group.add_payment(request.json["name"], request.json["total_amount"])
    
    return jsonify(message="Group payment was created successfully", group_payment=group_payment.__dict__)

@groups_blueprint.patch("/<group_id>/payments/<payment_id>")
def patch_group_payment(group_id: int, payment_id: int):
    if not request.json:
        raise Bad_Request("Missing information")

    group_payment = Group_Payment.get_by_id(payment_id, group_id)
    group_payment.edit(request.json.get("name"), request.json.get("total_amount"))
    
    return jsonify(message="Changes were made successfully", group_payment=group_payment), 200

#! /groups/<group_id>/payments/<group_payment_id>/member_payments

@groups_blueprint.get("/groups/<group_id>/payments/<group_payment_id>")
def get_member_payments(group_id: int, group_payment_id: int):
    """Get a group payment's member payments"""
    group_payment = Group_Payment.get_by_id(group_payment_id, group_id)
    
    return jsonify(member_payments=group_payment.member_payments)

#! /groups/<group_id>/payments/<group_payment_id>/member_payments/members/<member_id>

@groups_blueprint.get("/groups/<group_id>/payments/<group_payment_id>/member_payments/members/<member_id>")
def get_member_payment(group_payment_id: int, member_id):
    member_payment = Member_Payment.get_by_id(member_id, group_payment_id)
    
    return jsonify(member_payment=member_payment)

@groups_blueprint.get("/groups/<group_id>/payments/<group_payment_id>/member_payments/members/<member_id>")
def make_member_payment(group_payment_id: int, member_id):
    member_payment = Member_Payment.get_by_id(member_id, group_payment_id)
    
    return jsonify(member_payment=member_payment)

