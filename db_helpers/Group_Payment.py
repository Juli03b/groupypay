"""Module for Group_Payments model"""

from decimal import Decimal
from db_helpers.Member_Payment import Member_Payment
from models.Member_Payments import Member_Payments
from exceptions.Bad_Request import Bad_Request
from sqlalchemy.exc import IntegrityError
from models.Group_Payments import Group_Payments, db
from dataclasses import dataclass
from sqlalchemy.sql.functions import now

@dataclass
class Group_Payment:
    
    id: int
    group_id: int
    name: str
    member_id: int
    total_amount: float
    member_payments: Member_Payment
    created_on: str
    member: int
    
    """Class for logic abstraction from views"""
    
    def __init__(self, payment: Group_Payments):
        self.id = payment.id
        self.group_id = payment.group_id
        self.name = payment.name
        self.member_id = payment.member_id
        self.total_amount = float(payment.total_amount)
        self.member_payments = [Member_Payment(payment) for payment in payment.member_payments]
        self.created_on = payment.created_on
        self.member = payment.member
        self.key = (self.id, self.group_id)
    
    def __repr__(self) -> str:
        return f"<Group_Payment id={self.id} group_id={self.group_id} name={self.name} total_amount={self.total_amount} member_payments={self.member_payments} created_on={self.created_on}>"
    
    @classmethod
    def get_by_id(cls, id: int, group_id: int):
        """Return a user using id and group_id"""
        payment: Group_Payments = Group_Payments.query.get((id, group_id))
        
        return cls(payment)
 
    def edit(self, name: str=None, total_amount=None) -> None:
        """Edit payment using id"""
        payment: Group_Payments = Group_Payments.query.filter_by(id=self.id, group_id=self.group_id).first()
        payment.name = self.name = name or payment.name
        payment.total_amount = self.total_amount = total_amount or payment.total_amount

        try:
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            [message] = error.orig.args

            raise Bad_Request(message, "Database error", pgcode=error.orig.pgcode) from error

    def delete(self) -> None:
        """Delete payment using id"""
        
        Group_Payments.query.filter_by(id=self.id, group_id=self.group_id).delete()
        db.session.commit()
        
    def add_member_payments(self, member_payments):
        """Add member payments"""
        group_payment: Group_Payments = Group_Payments.query.filter_by(id=self.id, group_id=self.group_id).first()
        
        for member_id in member_payments:
            is_payer = int(member_id) == group_payment.member_id

            member_payment: Member_Payments = Member_Payments(
                member_id=member_id, 
                group_payment_id=self.group_id, 
                amount=member_payments[member_id],
                paid=is_payer,
                paid_on=now() if is_payer else None
            )
            group_payment.member_payments.append(member_payment)
            
        db.session.add(group_payment)
        
        try:
            db.session.commit()
            self.member_payments = [Member_Payment(member_payment) for member_payment in group_payment.member_payments]
        except IntegrityError as error:
            db.session.rollback()
            [message] = error.orig.args

            raise Bad_Request(message, "Database error", pgcode=error.orig.pgcode) from error

    def get_member_payment(self, member_id):
        member_payment = Member_Payments.query.filter_by(group_payment_id=self.id, member_id=member_id).first()
        
        return Member_Payment(member_payment)