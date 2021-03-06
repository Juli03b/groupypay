from dataclasses import dataclass
from decimal import Decimal
import json
from models.main import db, BaseModel
from sqlalchemy.sql.functions import now

@dataclass
class Member_Payments(BaseModel):
    __tablename__ = "member_payments"

    member_id: int = db.Column(
        db.Integer(),
        db.ForeignKey("group_members.id", ondelete="CASCADE"),
        primary_key=True
    )
    
    group_payment_id: int = db.Column(
        db.Integer(),
        db.ForeignKey("group_payments.id", ondelete="CASCADE"),
        primary_key=True
    )

    amount: str = db.Column(
        db.String(),
        nullable=False
    )
    
    created_on = db.Column(
        db.DateTime(timezone=True),
        default=now()
    )

    paid_on = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )
    
    paid: bool = db.Column(
        db.Boolean(),
        default=False,
        nullable=True
    )
    
    def __repr__(self):
        return f'<Member_Payments member_id={self.member_id} group_payment_id={self.group_payment_id} amount={self.amount} created_on={self.created_on} >'
