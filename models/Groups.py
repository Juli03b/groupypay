from models.main import db
from sqlalchemy.sql.functions import now
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True)
    
    name = db.Column(
        db.String(55),
        nullable=False
    )

    email = db.Column(
        db.String(127),
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String(),
        nullable=False
    )

    phone_number = db.Column(
        db.String(),
        nullable=True,
        unique=True
    )

    created_on = db.Column(
        db.DateTime(timezone=True),
        default=now()
    )

    def __repr__(self):
        return f'<User id={self.id} first_name={self.first_name} last_name={self.last_name} email={self.email} phone_number={self.phone_number}>'
