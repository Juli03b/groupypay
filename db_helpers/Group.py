"""Module for Group class"""

from typing import List
from Group_Members import Group_Members
from models.Users import Users, db
from models.Groups import Groups
from models.Group_Payments import Group_Payments
from exceptions.BadRequest import BadRequest
from sqlalchemy.exc import IntegrityError

class Group:
    """Class for logic abstraction from views"""
    
    def __init__(self, group: Groups):
        self.id = group.id
        self.name = group.name
        self.user_id = group.user_id
        self.name = group.name
        self.description = group.description
        self.created_on = group.created_on
        self.members: List[Group_Members] = group.members
        self.payments: List[Group_Payments] = group.payments

    ### Group Logic ###
    
    @classmethod
    def get_group_by_id(cls, id: int):
        """Return a group using an id"""
        group = Groups.query.filter_by(id=id)

        return cls(group)
    
    def edit(self, name: str=None, description: str=None) -> None:
        """Edit group"""
        group: Groups = Groups.query.filter_by(id=self.id)
        group.name = name or group.name
        group.description = description or group.description
    
    ### Payment Logic ###
    
    @staticmethod
    def edit_payment(id: int, name: str=None, total_amount=None) -> Group_Payments:
        """Edit and return payment using given id"""
        payment: Group_Payments = Group_Payments.query.filter_by(id=id)
        payment.name = name or payment.name
        payment.total_amount = total_amount or payment.total_amount
        
        return payment
    
    @staticmethod
    def delete_payment(id: int) -> None:
        """Delete payment using id"""
        Group_Payments.query.filter_by(id=id).delete()
    
    def add_payment(self, name: str, total_amount) -> Group_Payments:
        """Create and add payment to group"""
        payment = Group_Payments(
            name=name,
            total_amount=total_amount
        )
        
        self.payments.append(payment)
        db.session.commit()
        
        return payment
    
    ### Member Logic ###
    
    @staticmethod
    def edit_member(id: int, name:str=None, email: str=None, phone_number: str=None) -> Group_Members:
        """Edit and return member using given id"""
        member: Group_Members = Group_Members.query.filter_by(id=id)
        member.name = name or member.name
        member.email = email or member.email
        member.phone_number = phone_number or member.phone_number
        
        db.session.commit()
        
        return member
    
    @staticmethod
    def delete_member(id: int) -> None:
        """Delete member using id"""
        Group_Members.query.filter_by(id=id).delete()
    
    def add_member(self, name: str, email: str, phone_number: str) -> Group_Members:
        """Add member to the group and return member"""
        member: Group_Members = Group_Members(
            name=name,
            email=email,
            phone_number=phone_number
        )
        
        self.members.append(member)
        db.session.commit()
        
        return member
    
    ### Member Payment Logic ###
    
    