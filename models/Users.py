from phonenumbers.phonenumberutil import NumberParseException, format_number
from sqlalchemy import exc
from models.main import db
from sqlalchemy.sql.functions import now
from flask_bcrypt import Bcrypt
from phone_number_validation import validate_phone_number

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
        db.String(127),
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
    def sign_up(cls, first_name, last_name, email, password, phone_number=None):
        # Extra information to be returned, can be empty
        warning = None

        # Create hashed password from plain text password
        hashed_password = bcrypt.generate_password_hash(password).decode("UTF-8")
        
        # Parse and validate phone number if exists, set to false if parsing or validation fails
        if phone_number:
            formated_number, msg  = validate_phone_number(phone_number)
            phone_number = formated_number
            warning = dict(message=msg, cause="phone_number")
        else:
            warning = dict(message="Phone number was not provided, none saved", cause="phone_number")

        # Instantiate a user
        user = cls(
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            password=hashed_password, 
            phone_number=phone_number)

        # Add user object to db session
        db.session.add(user)

        return user, warning
    