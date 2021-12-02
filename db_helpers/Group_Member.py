"""Module for Group_Members model"""

from models.Member_Payments import Member_Payments
from db_helpers.Member_Payment import Member_Payment
from exceptions.BadRequest import BadRequest
from sqlalchemy.exc import IntegrityError
from models.Group_Members import Group_Members, db

class Group_Member:
    """Class for logic abstraction from views"""
    
    def __init__(self, member: Group_Members):
        self.id = member.id
        self.group_id = member.group_id
        self.name = member.name
        self.email = member.email
        self.phone_number = member.phone_number
        self.added_on = member.added_on
    
    def __repr__(self) -> str:
        return f"<Group_Member id={self.id} group_id={self.group_id} name={self.name} email={self.email} phone_number={self.phone_number} added_on={self.added_on}>"
    
    @classmethod
    def get_by_id(cls, id: str):
        """Return a user using an id"""
        
        payment: Group_Members = Group_Members.query.filter_by(id=id)
        
        return cls(payment)
 
    def edit(self, name:str=None, email: str=None, phone_number: str=None) -> None:
        """Edit member using id"""
        member: Group_Members = Group_Members.query.filter_by(id=self.id)
        member.name = name or member.name
        member.email = email or member.email
        member.phone_number = phone_number or member.phone_number
        
        db.session.commit()
        
    def delete(self) -> None:
        """Delete payment using id"""
        
        Group_Members.query.filter_by(id=self.id).delete()
        
    def add_payment(self, group_payment_id: int, amount: float or int) -> Member_Payment:
        member_payment: Member_Payments = Member_Payments(
            member_id=self.id,
            group_payment_id=group_payment_id,
            amount=amount
        )
        
        db.session.add(member_payment)
        db.session.commit()
        
        return Member_Payment(member_payment)