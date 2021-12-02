"""Module for User class"""

from models.Groups import Groups
from db_helpers.Group import Group
from exceptions.BadRequest import BadRequest
from sqlalchemy.exc import IntegrityError
from models.Users import Users, db

class User:
    """Class for logic abstraction from views"""
    
    def __init__(self, user: Users):
        self.id = user.id
        self.name = user.name
        self.email = user.email
        self.phone_number = user.phone_number
        self.groups = user.groups

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} name={self.name} phone_number={self.phone_number}>"
    
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
    
    @classmethod
    def get_by_id(cls, id: str):
        """Return a user using an id"""
        
        user: Users = Users.query.filter_by(id=id).first()
        
        return cls(user)
    
    def edit(self, name: str=None, email: str=None, phone_number: str=None) -> None:
        """Edit group"""
        user: Users = Users.query.filter_by(id=self.id).first()
        user.name = self.name = name or user.name
        user.email = self.email = email or user.email
        user.phone_number = self.phone_number = phone_number or user.phone_number
        
        db.session.commit()
    
    def delete(self):
        Users.query.filter_by(id=self.id).delete()
    
    def make_group(self, name: str, description: str) -> Groups:
        """Make a group"""
        group = Groups(
            user_id=self.id,
            name=name,
            description=description
        )
        
        db.session.add(group)
        db.session.commit()
        
        return Group(group)