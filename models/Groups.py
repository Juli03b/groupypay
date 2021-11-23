from models.main import db
from sqlalchemy.sql.functions import now
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class Groups(db.Model):
    __tablename__ = "groups"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    
    name = db.Column(
        db.String(30),
        nullable=False
    )

    description = db.Column(
        db.String(200),
        nullable=True
    )
    
    created_on = db.Column(
        db.DateTime(timezone=True),
        default=now()
    )

    payments = db.relationship("Group_Payments", backref="groups", passive_deletes=True)
    members = db.relationship("Group_Members", backref="groups", passive_deletes=True)
    
    def __repr__(self):
        return f'<Group id={self.id} first_name={self.name} last_name={self.last_name} email={self.email} phone_number={self.created_on}>'
