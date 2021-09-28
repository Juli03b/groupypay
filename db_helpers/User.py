import email_validator
from exceptions.BadRequest import BadRequest
from sqlalchemy.exc import IntegrityError
from models.Users import Users
from app import db

class User:
    """Class for logic abstraction from views"""
    email = None
    first_name = None
    last_name = None
    email = None
    phone_number = None

    def __init__(self, user: Users):
        self.email = user.email
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.email = user.email
        self.phone_number = user.phone_number

    @classmethod
    def sign_up(cls, **validated_json):

        # Create user
        user = Users.sign_up(**validated_json)

        # Attempt making entry to db. If failed, return error with message and pg code
        try:
            db.session.commit()
        except IntegrityError as e:

            db.session.rollback()
            [message] = e.orig.args

            raise BadRequest(message, "Invalid data", pgcode=e.orig.pgcode)

        return cls(user)