from typing import List
from models.Member_Payments import Member_Payments
from models.main import db, BaseModel
from sqlalchemy.sql.functions import now

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
    member_id_paid = db.Column(
        db.Integer(),
        db.ForeignKey("group_members.id", ondelete="CASCADE"),
        primary_key=True
    )
    name: str = db.Column(
        db.String(45),
        nullable=False
    )
    total_amount: float = db.Column(
        db.Numeric(15, 6),
        nullable=True
    )
    created_on = db.Column(
        db.DateTime(timezone=True),
        default=now()
    )
    
    # group = db.relationship("Groups", backref="group_payments", passive_deletes=True)
    member_payments: List[Member_Payments] = db.relationship("Member_Payments", backref="group_members_payments", passive_deletes=True)

    def __repr__(self):
        return f'<Group_Payments id={self.id} group_id={self.group_id} member_id_paid={self.member_id_paid} name={self.name} total_amount={self.total_amount} created_on={self.created_on} member_payments={self.member_payments}>'
