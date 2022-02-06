from decimal import Decimal
from typing import List
from models.Member_Payments import Member_Payments
from models.main import db, BaseModel
from sqlalchemy.sql.functions import now
from dataclasses import dataclass

@dataclass
class Group_Payments(BaseModel):
    __tablename__ = "group_payments"

    id: int = db.Column(
        db.Integer(),
        primary_key=True,
        autoincrement=True,
        unique=True
    )
    group_id: int = db.Column(
        db.Integer(),
        db.ForeignKey("groups.id", ondelete="CASCADE"),
        primary_key=True
    )
    member_id = db.Column(
        db.Integer(),
        db.ForeignKey("group_members.id", ondelete="CASCADE"),
    )
    name: str = db.Column(
        db.String(45),
        nullable=False
    )
    total_amount: str = db.Column(
        db.String(),
        nullable=True
    )
    created_on: str = db.Column(
        db.DateTime(timezone=True),
        default=now()
    )
    
    # group = db.relationship("Groups", backref="group_payments", passive_deletes=True)
    member = db.relationship("Group_Members", backref="group_payment", passive_deletes=True)

    member_payments: List[Member_Payments] = db.relationship("Member_Payments", backref="group_members_payments", passive_deletes=True)

    def __repr__(self):
        return f'<Group_Payments id={self.id} group_id={self.group_id} member_id={self.member_id} name={self.name} total_amount={self.total_amount} created_on={self.created_on} member_payments={self.member_payments}>'
