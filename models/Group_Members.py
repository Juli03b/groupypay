from models.main import db
from sqlalchemy.sql.functions import now

class Users(db.Model):
    __tablename__ = "group_members"

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True)
    
    group_id = db.Column(
        db.Integer,
        db.ForeignKey("group.id", ondelete="CASCADE"),
        primary_key=True
    )
    
    name = db.Column(
        db.String(55),
        nullable=False
    )
    
    email = db.Column(
        db.String(127),
        nullable=False
    )

    phone_number = db.Column(
        db.String(),
        nullable=True,
    )

    added_on = db.Column(
        db.DateTime(timezone=True),
        default=now()
    )

    members = db.relationship("Member_Payments", backref="group_members", passive_deletes=True)

    def __repr__(self):
        return f'<Group_Members id={self.id} group_id={self.group_id} name={self.name} email={self.email} phone_number={self.phone_number} added_on={self.added_on}>'
        