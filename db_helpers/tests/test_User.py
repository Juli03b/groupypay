"""Unit test for User class"""

import sys

sys.path.append("../..")

from models.Users import Users
from models.Groups import Groups
from unittest import TestCase
from app import app, connect_db, db
from db_helpers.User import User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///groupypay_test'
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app), db.drop_all(), db.create_all()

demo_user_json = {
    "name": "Julio",
    "email": "julio@g3mail.com",
    "password": "123Securepassword321",
    "phone_number": "938-323-321"
}

class UserTestCase(TestCase):
    
    def setUp(self) -> None:
        """Create a user"""
        Users.query.delete()
        db.session.commit()
        
        self.user: User = User.sign_up(**demo_user_json)

    def tearDown(self) -> None:
        """Rollback session"""
        db.session.rollback()
    
    def test_user(self) -> None:
        """Test if user exists"""
        self.assertTrue(self.user)
        user_from_db: Users = Users.query.filter_by(id=self.user.id).first()
        self.assertEqual(self.user.id, user_from_db.id)
    
    def test_get_by_id(self) -> None:
        """Test get_by_id method"""

        user = User.get_by_id(self.user.id)
        
        self.assertEqual(user.id, self.user.id)

    def test_edit(self) -> None:
        """Test that changes appear in both User and Users"""
        self.user.edit("Oiluj", "emailaemei", "313232")
        user_from_db: Users = Users.query.filter_by(id=self.user.id).first()
        
        self.assertEqual(self.user.name, user_from_db.name, "Test that name change appears in database and User")
        self.assertEqual(self.user.email, user_from_db.email, "Test that email change appears in database and User")
        self.assertEqual(self.user.phone_number, user_from_db.phone_number, 
                         "Test that phone number change appears in database and User")
    
    def test_make_group(self) -> None:
        """Test make_group"""
        group = self.user.make_group("New group!", "I made a group!")
        group_from_db: Groups = Groups.query.filter_by(id=group.id).first()
        self.assertEqual(group.id, group_from_db.id, "Test that the group apears in database")