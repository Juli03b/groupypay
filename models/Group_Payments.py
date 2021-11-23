from models.main import db
from sqlalchemy.sql.functions import now
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class Group_Payments(db.Model):
    __tablename__ = "group_payments"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    
    group_id = db.Column(
        db.Integer,
        db.ForeignKey("group.id", ondelete="CASCADE"),
        primary_key=True
    )

    total_amount = db.Column(
        db.Numeric(15, 6),
        nullable=True
    )
    
    created_on = db.Column(
        db.DateTime(timezone=True),
        default=now()
    )

    
    def __repr__(self):
        return f'<Group_Payments id={self.id} group_id={self.group_id} total_amount={self.total_amount} created_on={self.created_on} >'
