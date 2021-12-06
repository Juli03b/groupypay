"""Module for Member_Payments model"""

from sqlalchemy.sql.functions import now
from models.Member_Payments import Member_Payments
from exceptions.Bad_Request import Bad_Request
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
        self.key = (self.member_id, self.group_payment_id)

    def __repr__(self) -> str:
        return f"<Member_Payment member_id={self.member_id} group_payment_id={self.group_payment_id} amount={self.amount} paid_on={self.paid_on} paid={self.paid} created_on={self.created_on}>"
    
    @classmethod
    def get_by_id(cls, member_id: str, group_payment_id: str):
        """Return a user using composite string: (member_id, group_payment_id)"""
        
        payment: Member_Payments = Member_Payments.query.get((member_id, group_payment_id))
        
        return cls(payment)
        
    def edit(self, amount) -> None:
        """Edit payment using id"""
        member_payment: Member_Payments = Member_Payments.query.get(self.key)
        member_payment.amount = self.amount = amount or member_payment.amount
        
        try:
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            [message] = error.orig.args

            raise Bad_Request(message, "Database error", pgcode=error.orig.pgcode) from error
        
    def delete(self) -> None:
        """Delete payment using id"""
        Member_Payments.query.filter_by(
            member_id=self.member_id,
            group_payment_id = self.group_payment_id
        ).delete()
        
        db.session.commit()
    
    def pay(self) -> None:
        """Set member_payment to paid"""
        member_payment: Member_Payments = Member_Payments.query.get(self.key)
        member_payment.paid = self.paid = True
        member_payment.paid_on = self.paid_on = now()