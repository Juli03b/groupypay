from os import environ
from flask import Flask
from models.main import connect_db, db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from user import sign_up

app = Flask(__name__)

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = environ.get('SECRET_KEY', 'its_a_secret')
app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY", "secret-af")
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'postgresql:///groupypay')

jwt = JWTManager(app)

connect_db(app)
db.create_all()

@app.get("/")
def home():
    return "NONE"

@app.post("/users")
def _():
    return sign_up()