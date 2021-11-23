from models.main import db
from sqlalchemy.sql.functions import now

class Group_Payments(db.Model):
    __tablename__ = "group_payments"

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("group_members.id", ondelete="CASCADE"),
        primary_key=True
    )
    
    group_payment_id = db.Column(
        db.Integer,
        db.ForeignKey("group_payments.id", ondelete="CASCADE"),
        primary_key=True
    )

    amount = db.Column(
        db.Numeric(15, 6),
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
    
    paid = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )
    
    def __repr__(self):
        return f'<Member_Payments id={self.id} group_id={self.group_id} total_amount={self.total_amount} created_on={self.created_on} >'