"""Module for User class"""

from typing import Any, List
from flask_jwt_extended.utils import decode_token
from db_helpers.Member_Payment import Member_Payment
from exceptions.Unauthorized import Unauthorized
from exceptions.Bad_Request import Bad_Request
from models.Group_Members import Group_Members
from models.Member_Payments import Member_Payments
from models.Groups import Groups
from models.Users import Users, db
from db_helpers.Group import Group
from sqlalchemy.exc import IntegrityError
from dataclasses import dataclass

@dataclass
class User:
    """Class for logic abstraction from views"""
    
    id: int
    name: str
    email: str
    phone_number: str
    groups: Any
    owed_payments: Any
    
    def __init__(self, user: Users):
        self.id = user.id
        self.name = user.name
        self.email = user.email
        self.phone_number = user.phone_number
        self.password = user.password
        self.groups = [Group(group) for group in user.groups]
        owed_payments = db.session.query(Member_Payments).\
            join(Group_Members, Member_Payments.member_id==Group_Members.id).\
            group_by(Member_Payments).\
            filter(Group_Members.email==user.email).\
            all()
        self.owed_payments = [Member_Payment(member_payment) for member_payment in owed_payments]
                             
    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} name={self.name} phone_number={self.phone_number} groups={self.groups}>"
    
    @classmethod
    def authenticate_token(cls, token: str):
        """Return a User using a token"""
        user = decode_token(token)

        return cls.get_by_email(user["sub"]["email"])
    
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

            raise Bad_Request(message, "Database error", pgcode=error.orig.pgcode) from error
        
        return cls(user)
    
    @classmethod
    def sign_in(cls, email: str, password: str):
        """Return user using email and password, raise exception incase of invalid credentaials"""
        
        if not Users.query.filter_by(email=email).count():
            raise Unauthorized("No user with that email has been found", "Invalid credentials")
        
        user = Users.authenticate(email, password)

        if not user:
            raise Unauthorized("Wrong password", "Invalid credentials")
        
        return cls(user)
    
    @classmethod
    def get_by_id(cls, id: int):
        """Return a user using an id"""
        user: Users = Users.query.filter_by(id=id).first()
        if not user:
            raise Bad_Request(f"User with id {id} does not exist")
        return cls(user)
    
    @classmethod
    def get_by_email(cls, email: str):
        """Return a user using an email"""
        user: Users = Users.query.filter_by(email=email).first()
        
        if not user:
            raise Bad_Request(f"User with email {email} does not exist")
                
        return cls(user)
    
    @classmethod
    def search_users(cls, name: str):
        """Search and return users"""
        
        users: List[Users] = Users.query.filter(Users.tags.like(name)).all()
        
        return users
    
    def edit(self, name: str=None, email: str=None, phone_number: str=None, password: str=None) -> None:
        """Edit group"""
        user: Users = Users.query.filter_by(id=self.id).first()
        user.name = self.name = name or user.name
        user.email = self.email = email or user.email
        user.phone_number = self.phone_number = phone_number
        
        if password:
            password = Users.make_hashed_password(password)

        user.password = self.password = user.password
        
        try:
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            [message] = error.orig.args

            raise Bad_Request(message, "Database error", pgcode=error.orig.pgcode) from error
    
    def delete(self) -> None:
        """Delete user"""
        Users.query.filter_by(id=self.id).delete()
        db.session.commit()
    
    def get_group(self, id, email:str or None, secret_code: str or None=None):
        """Get user's group"""
        print("EMAIL!", email)
        group: Group = Group.get_with_auth(id, email, secret_code)
        return group
        
    def make_group(self, name: str, description: str, secret_code: int) -> Group:
        """Make a group"""
        group = Groups(
            user_id=self.id,
            name=name,
            description=description,
            secret_code=secret_code
        )

        db.session.add(group)
        
        try:
            db.session.commit()
        except IntegrityError as error:

            db.session.rollback()
            [message] = error.orig.args

            raise Bad_Request(message, "Database error", pgcode=error.orig.pgcode) from error
        
        return Group(group)