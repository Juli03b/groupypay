from json_validation import validate_json
from os import environ
from flask import Flask, request
from models.Users import Users
from flask.json import jsonify
from models.main import connect_db, db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from email_validator import validate_email, EmailNotValidError
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
def sign_up(): 
    valid_json, msg = validate_json(request.json, "user_schema")

    # Check if JSON request is valid, return error and HTTP code accordingly
    if not valid_json:
        return jsonify(error=msg), 400
    try:
        valid_email = validate_email(request.json["email"])
        print(valid_email.email)
    except EmailNotValidError as e:
        return jsonify(error=dict(message=str(e), cause="email")), 400
    # Create user
    user, warning = Users.sign_up(**request.json)

    # Attempt making entry to db, return error and HTTP code if failed
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()

        [message] = e.orig.args

        return jsonify(error=dict(message=message, pg_code=e.orig.pgcode)), 409

    # Create jwt token containing user's email
    access_token = create_access_token(user.email)

    return jsonify(message="Sign up successful", warning=warning, access_token=access_token)
