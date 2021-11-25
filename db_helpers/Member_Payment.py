"""Module for Member_Payments model"""

from Member_Payments import Member_Payments
from exceptions.BadRequest import BadRequest
from sqlalchemy.exc import IntegrityError
from models.Group_Payments import Group_Payments, db

class Member_Payment:
    """Class for logic abstraction from views"""
    
    def __init__(self, payment: Member_Payments):
        self.member_id = payment.member_id
        self.group_payment_id = payment.group_payment_id
        self.amount = payment.amount
        self.paid_on = payment.paid_on
        self.paid = payment.paid
        self.created_on = payment.created_on
    
    @classmethod
    def get_by_id(cls, id: str):
        """Return a user using an id"""
        
        payment: Member_Payments = Member_Payments.query.filter_by(id=id)
        
        return cls(payment)
 
    def edit(self, amount) -> None:
        """Edit payment using id"""
        member_payment: Member_Payments = Member_Payments.query.filter_by(id=id)
        member_payment.amount = self.amount = amount or member_payment.amount
        
        db.session.commit()
        
    def delete(self) -> None:
        """Delete payment using id"""
        
        Member_Payments.query.filter_by(id=self.id).delete()