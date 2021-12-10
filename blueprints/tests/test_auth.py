"""Test auth views"""

import os
import sys


sys.path.append("../..")

from unittest import TestCase
from app import db, connect_db, app
from models.Users import Users
from db_helpers.User import User
from flask.json import dumps

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///groupypay_test'
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app), db.drop_all(), db.create_all()
os.chdir("../..") # Change directory to groupypay to access json

class authTestCase(TestCase):

    def setUp(self):
        """Create user"""
        Users.query.delete()
        db.session.commit()
        self.password = "123456"
        self.user = User.sign_up(**dict(name="t3st", email="t33st@gmail.com", password=self.password, phone_number="2313232"))

    def tearDown(self):
        """Rollback session"""
        db.session.rollback()

    def test_signup(self):
        """Test sign up view"""
        data = dict(name="3424", email="JDWWO@gmail.com", password="231313232", phone_number="+1 831-322-2311")
        with app.test_client() as client:
            # os.chdir("../..") # Change directory to groupypay to access json
            res = client.post('/auth/sign-up', data=dumps(data), content_type='application/json')
            json = res.get_json()

            self.assertEqual(res.status_code, 201, "Test that user was signed up successfully")
            self.assertIn("access_token", json, "Test that access_token exists in json")

            # Testing duplicate email
            data = dict(password="4434343", name=self.user.name, email=self.user.email)
            res = client.post('/auth/sign-up', data=dumps(data), content_type='application/json')
            json = res.get_json()

            self.assertEqual(res.status_code, 400, "Test that Bad Request was returned")
            self.assertEqual(json["error"]["pgcode"], "23505", "Test that psql error is correct (Duplicate email)")

            # Testing invalid email domain
            data = dict(password="4434343", name=self.user.name, email="email@.com")
            res = client.post('/auth/sign-up', data=dumps(data), content_type='application/json')
            json = res.get_json()

            self.assertEqual(res.status_code, 400, "Test that Bad Request was returned")
            self.assertEqual(json["error"]["cause"], "email", "Test that email is error")

            # Testing short password (min is 5)
            data = dict( password="1234", name="new_ users", email="USER_NEW@new.com")
            res = client.post('/auth/sign-up', data=dumps(data), content_type='application/json')
            json = res.get_json()
            
            self.assertEqual(res.status_code, 400, "Test that Bad Request was returned")
            self.assertEqual(json["error"]["message"], "'1234' is too short", "Test that the right message was returned")
    def test_get_token(self):
        """Test token view"""
        
        with app.test_client() as client:

            res = client.post('/auth/token', data=dumps(dict(email=self.user.email, password=self.password)), content_type='application/json')
            json = res.get_json()
            
            self.assertIn("token", json, "Test that JSON contains token")
            self.assertIn("user_id", json, "Test that JSON contains user_id")
            self.assertEqual(res.status_code, 200, "Test that status code is correct")
            
            # Test non-existent user - email
            res = client.post('/auth/token', data=dumps(dict(email="does not exist", password=self.password)), content_type='application/json')
            json = res.get_json()

            self.assertEqual(json["error"]["message"], "No user with that email has been found")
            self.assertEqual(res.status_code, 401, "Test that status code is correct")
            
            # Test wrong password
            res = client.post('/auth/token', data=dumps(dict(email=self.user.email, password="WRONGPASSWORD")), content_type='application/json')
            json = res.get_json()

            self.assertEqual(json["error"]["message"], 'Wrong password')
            self.assertEqual(res.status_code, 401, "Test that status code is correct")