"""Unit test for Group_Member class"""

import sys
from flask.scaffold import setupmethod

from db_helpers.Group_Member import Group_Member

sys.path.append("../..")

from unittest import TestCase
from app import app, connect_db, db
from models.Group_Members import Group_Members
from models.Users import Users
from models.Groups import Groups
from models.Group_Payments import Group_Payments
from db_helpers.Group import Group
from db_helpers.User import User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///groupypay_test'
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app), db.drop_all(), db.create_all()

demo_user_json = {
    "name": "Julio",
    "email": "julio@gmail.com",
    "password": "123Securepassword321",
    "phone_number": "938-323-321"
}

class Group_MemberTestCase(TestCase):
    @setupmethod
    def setUpClass(cls):
        """Create user and group"""
        cls.user: User = User.sign_up(**demo_user_json)
        cls.group: Group = cls.user.make_group("New group!", "I made a group!")

    def setUp(self):
        """Create group member"""
        self.group_member = self.group.add_member("Juli0", "Ju110@gmail.com", "317817223")

    def tearDown(self) -> None:
        """Delete all group members"""
        Group_Members.query.delete()
        db.session.commit()
        db.session.rollback()
    
    def test_group_member(self) -> None:
        """Test if group_member exists"""
        group_member_from_db: Group_Members = Group_Members.query.filter_by(id=self.group_member.id).first()

        self.assertEqual(self.group_member.id, group_member_from_db.id, "Test that group member can be found in db")
        
    def test_edit(self) -> None: