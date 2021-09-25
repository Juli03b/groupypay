from os import environ
from flask import Flask, request
from models.Users import Users
from flask.json import jsonify
from models.main import connect_db, db
from sqlalchemy.exc import IntegrityError
from jsonschema import validate, ValidationError, SchemaError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
import json
app = Flask(__name__)

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = environ.get('SECRET_KEY', 'its_a_secret')
app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY", "secret-af")
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'postgresql:///groupypay')

jwt = JWTManager(app)

connect_db(app)
db.create_all()

with open("./json_schemas/user_schema.json", "r") as js:
    user_schema = json.load(js)
@app.get("/")
def home():
    return "NONE"

@app.post("/users")
def signUp():
    try:
        valid_input = validate(request.json, user_schema)
        return jsonify(valid_input)
    
    except (ValidationError, SchemaError) as e:
        return jsonify(dir(e), str(e.message))
        
    user = Users.signUp(
        first_name=request.json.get("first_name"), 
        last_name=request.json.get("last_name"), 
        email=request.json.get("email"), 
        password=request.json.get("password"), 
        phone_number=request.json.get("phone_number"))

    try:
        db.session.commit()
    except IntegrityError as e:
        print("EEEEEEEEEEEEEEEE", e)
        db.session.rollback()
        [message] = e.orig.args
        error_code = e.orig.pgcode

        return jsonify(message, error_code), 409
    print(user)
    access_token = create_access_token(user.email)
    return jsonify(access_token=access_token)
