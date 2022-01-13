"""Test users views"""

import os
import sys

from flask_jwt_extended.utils import decode_token

sys.path.append("../..")

from unittest import TestCase
from app import db, connect_db, app
from models.Users import Users
from flask.json import dumps

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///groupypay_test'
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app), db.drop_all(), db.create_all()

class usersTestCase(TestCase):
 
    def setUp(self):
        """Create user"""
        Users.query.delete()
        db.session.commit()
        
        self.user = dict(name="3424", email="JDWWO@gmail.com", password="231313232", phone_number="+1 831-322-2311")
        
        with app.test_client() as client:
            res = client.post('/auth/sign-up', data=dumps(self.user), content_type='application/json')
            json = res.get_json()
            self.access_token = json.get("access_token")
            
    def tearDown(self):
        """Rollback session"""
        db.session.rollback()

    def test_get_user(self):
        """Test get_user view"""
        with app.test_client() as client:
            res = client.get(f'/users/{self.user["email"]}', content_type='application/json')
            json = res.get_json()
            
            self.assertEqual(json["name"], self.user["name"])

    def test_patch_user(self):
        """Test patch_user view"""
        patch_data = dict(name="NEW_ name", token=self.access_token)
        
        with app.test_client() as client:
            
            res = client.patch(f'/users/{self.user["email"]}', data=dumps(patch_data), content_type='application/json')
            json = res.get_json()
            
            self.assertEqual(res.status_code, 200)
            self.assertEqual(json["name"], "NEW_ name")