"""Module for Group_Payments model"""

from Member_Payments import Member_Payments
from exceptions.BadRequest import BadRequest
from sqlalchemy.exc import IntegrityError
from models.Group_Payments import Group_Payments, db

class Group_Payment:
    """Class for logic abstraction from views"""
    
    def __init__(self, payment: Group_Payments):
        self.id = payment.id
        self.group_id = payment.group_id
        self.name = payment.name
        self.total_amount = payment.email
        self.member_payments = payment.member_payments
        self.created_on = payment.created_on
    
    @classmethod
    def get_by_id(cls, id: str):
        """Return a user using an id"""
        
        payment: Group_Payments = Group_Payments.query.filter_by(id=id)
        
        return cls(payment)
 
    def edit(self, name: str=None, total_amount=None) -> None:
        """Edit payment using id"""
        payment: Group_Payments = Group_Payments.query.filter_by(id=id)
        payment.name = self.name = name or payment.name
        payment.total_amount = self.total_amount = total_amount or payment.total_amount

        db.session.commit()
        
    def delete(self) -> None:
        """Delete payment using id"""
        
        Group_Payments.query.filter_by(id=self.id).delete()