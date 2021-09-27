"""Main module for app setup"""

from os import environ
from flask import Flask
from flask_jwt_extended import JWTManager
from models.main import connect_db, db
from user import users

app = Flask(__name__)

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = environ.get('SECRET_KEY', 'its_a_secret')
app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY", "secret-af")
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'postgresql:///groupypay')

jwt = JWTManager(app)

connect_db(app)
db.create_all()

# Register blueprint for /users routes
app.register_blueprint(users, url_prefix="/users")
