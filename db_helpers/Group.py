"""Module for Group class"""

from typing import List
from Group_Members import Group_Members
from db_helpers.Group_Member import Group_Member
from db_helpers.Group_Payment import Group_Payment
from models.Groups import Groups, db
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
        
    @classmethod
    def get_by_id(cls, id: int):
        """Return a group using an id"""
        group = Groups.query.filter_by(id=id)

        return cls(group)
    
    def edit(self, name: str=None, description: str=None) -> None:
        """Edit group"""
        group: Groups = Groups.query.filter_by(id=self.id)
        group.name = self.name = name or group.name
        group.description = self.description = description or group.description
    
        db.session.commit()
    
    def add_payment(self, name: str, total_amount) -> Group_Payment:
        """Create and add payment to group"""
        payment = Group_Payments(
            name=name,
            total_amount=total_amount
        )
        
        self.payments.append(payment)
        db.session.commit()
        
        return Group_Payment(payment)
    
    def add_member(self, name: str, email: str, phone_number: str) -> Group_Member:
        """Add member to the group and return member"""
        member: Group_Members = Group_Members(
            name=name,
            email=email,
            phone_number=phone_number
        )
        
        self.members.append(member)
        db.session.commit()
        
        return Group_Member(member)