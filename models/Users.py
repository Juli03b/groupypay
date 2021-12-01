from models.main import db
from models.Groups import Groups
from sqlalchemy.sql.functions import now
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

class Users(db.Model):
    __tablename__ = "users"

    id: int = db.Column(
        db.Integer(), 
        primary_key=True, 
        autoincrement=True)
    
    name: str = db.Column(
        db.String(55),
        nullable=False
    )

    email: str = db.Column(
        db.String(127),
        nullable=False,
        unique=True
    )

    password: str = db.Column(
        db.String(),
        nullable=False
    )

    phone_number: str = db.Column(
        db.String(),
        nullable=True,
        unique=True
    )

    created_on = db.Column(
        db.DateTime(timezone=True),
        default=now()
    )

    groups = db.relationship("Groups", backref="users", passive_deletes=True)

    def __repr__(self):
        return f'<Users id={self.id} name={self.name} email={self.email} phone_number={self.phone_number} created_on={self.created_on}>'

    @classmethod
    def sign_up(cls, name: str, email: str, password: str, phone_number: str=None):

        # Create hashed password from plain text password
        hashed_password = bcrypt.generate_password_hash(password).decode("UTF-8")

        # Instantiate a user
        user = cls(
            name=name,
            email=email,
            password=hashed_password,
            phone_number=phone_number)

        # Add user object to db session
        db.session.add(user)

        return user

    @classmethod
    def sign_in(cls, email: str, password: str):
        """Sign in class method, returns user"""

        user: Users = cls.query.filter_by(email=email)
        if not user:
            verify_password = bcrypt.check_password_hash(user.password, password)
        
        