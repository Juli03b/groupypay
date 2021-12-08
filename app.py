"""Main module for app setup"""

from exceptions.Custom_Error import Custom_Error
from flask.json import jsonify
from os import environ
from flask import Flask
from flask_jwt_extended import JWTManager
from models.main import connect_db, db
from blueprints.users import users_blueprint
from blueprints.auth import auth_blueprint
from blueprints.groups import groups_blueprint

app = Flask(__name__)

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = environ.get('SECRET_KEY', 'its_a_secret')
app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY", "secret-af")
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'postgresql:///groupypay')

JWTManager(app)

# Connect db with app, create tables
connect_db(app), db.create_all() # pylint: disable=W0106

# Register blueprint for users routes
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(groups_blueprint, url_prefix="/groups")

@app.errorhandler(Custom_Error)
def error_handler(error):
    """Error handler for custom errors"""
    error, status_code = error.formated

    return jsonify(error=error), status_code
