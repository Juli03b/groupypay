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
    
    first_name = db.Column(
        db.String(20),
        nullable=False
    )

    last_name = db.Column(
        db.String(20),
        nullable=False
    )

    email = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String(),
        nullable=False
    )

    api_id = db.Column(
        db.String(),
        nullable=True,
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
        return f'<User id={self.id} email={self.email} first_name={self.first_name} last_name={self.last_name}>'

    @classmethod
    def signUp(cls, first_name, last_name, email, password, phone_number):

        hashed_password = bcrypt.generate_password_hash(password).decode("UTF-8")
        user = cls(
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            password=hashed_password, 
            phone_number=phone_number)

        db.session.add(user)

        return user
    