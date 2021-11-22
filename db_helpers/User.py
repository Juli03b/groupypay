"""Module for User class"""

from exceptions.BadRequest import BadRequest
from sqlalchemy.exc import IntegrityError
from models.Users import Users, db

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

    @staticmethod
    def get_user_by_id(id: str):
        """Return a list of all users"""
        
        user = Users.query.filter_by(id=id)
        del user.password
        
        return user

    @classmethod
    def sign_up(cls, **validated_json):
        """Sign up with validated json. Creates and returns user, or raises Bad Request error if there's a database error"""

        # Create user
        user = Users.sign_up(**validated_json)

        # Attempt making entry to db. If failed, return error with message and pg code
        try:
            db.session.commit()
        except IntegrityError as error:

            db.session.rollback()
            [message] = error.orig.args

            raise BadRequest(message, "Database error", pgcode=error.orig.pgcode) from error

        return cls(user)
    
    