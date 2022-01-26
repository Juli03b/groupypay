"""Module for Group class"""

from typing import List
from models.Group_Members import Group_Members
from db_helpers.Group_Member import Group_Member
from db_helpers.Group_Payment import Group_Payment
from models.Groups import Groups, db
from models.Group_Payments import Group_Payments
from exceptions.Bad_Request import Bad_Request
from sqlalchemy.exc import IntegrityError

row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

class Group:
    """Class for logic abstraction from views"""
    
    def __init__(self, group: Groups):
        self.id = group.id
        self.name = group.name
        self.user_id = group.user_id
        self.description = group.description
        self.created_on = group.created_on
        self.members: List[Group_Members] = list(map(row2dict, group.members))
        self.payments: List[Group_Payments] = list(map(row2dict, group.payments))
    
    def __repr__(self) -> str:
        return f"<Group id={self.id} name={self.name} user_id={self.user_id} description={self.description} created_on={self.created_on}>"
    
    @classmethod
    def get_by_id(cls, id: int):
        """Return a group using an id"""
        group = Groups.query.filter_by(id=id).first()
        if not group:
            raise Bad_Request(f"Group with id {id} does not exist")
        return cls(group)
    
    def edit(self, name: str=None, description: str=None) -> None:
        """Edit group"""
        group: Groups = Groups.query.filter_by(id=self.id).first()
        group.name = self.name = name or group.name
        group.description = self.description = description or group.description
    
        try:
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            [message] = error.orig.args

            raise Bad_Request(message, "Database error", pgcode=error.orig.pgcode) from error
    
    def delete(self) -> None:
        """Delete group"""
        Groups.query.filter_by(id=self.id).delete()
        db.session.commit()
        
    def add_payment(self, name: str, total_amount: float or int) -> Group_Payment:
        """Create and add payment to group"""
        payment = Group_Payments(
            group_id=self.id,
            name=name,
            total_amount=total_amount
        )
        
        db.session.add(payment)
        db.session.commit()
        print("PAYMENT!!!!!!!!!!!!!!!!!!!!!!!", payment, "PAYMENT!!!!!!!!!!!!!!!!!!!!!!!")
        return Group_Payment(payment)
    
    def add_member(self, name: str, email: str, phone_number: str) -> Group_Member:
        """Add member to the group and return member"""
        member: Group_Members = Group_Members(
            group_id=self.id,
            name=name,
            email=email,
            phone_number=phone_number
        )
        
        db.session.add(member)
        
        try:
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            [message] = error.orig.args

            raise Bad_Request(message, "Database error", pgcode=error.orig.pgcode) from error
        
        return Group_Member(member)