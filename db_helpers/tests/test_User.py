"""Unit test for User class methods"""

import sys

sys.path.extend(["../.."])

from unittest import TestCase
from app import app, connect_db, db
from models.Users import Users
from models.Groups import Groups
from models.Group_Members import Group_Members

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///groupypay_test'
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)

db.drop_all(), db.create_all()

class UserTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Create new user and group to add new members to"""
        Users.query.delete()
        # Create User
        cls.user_password = "123TESTING"
        cls.user_username = "THISISATEST"
        cls.user = Users.sign_up(
            name="TEST TESTING",
            email="test@test.com",
            password=cls.user_password, 
            phone_number="+1 213 999 2332"
        )

        db.session.add(cls.user)
        db.session.commit()

        cls.user_id = cls.user.id
        
        return super().setUpClass()
    
    def setUp(self) -> None:
        """Empty Groups table and add a member to it"""
        # Create Group
        self.group = Groups(
            name="TEST TESTING",
            user_id=self.user_id,
            description="TESTSTSETTSE"
        )

        db.session.add(self.group)
        db.session.commit()
        
        self.group_id = self.group.id
        
        # Add member to group
        self.member = Group_Members(
            name="TEEEST",
            email="TESTINGTON@TEST.com",
            phone_number="+132312323"
        )
        self.group.members.append(self.member)
        
        db.session.commit()
        
        self.member_id = self.member.id
    
    def tearDown(self) -> None:
        Groups.query.delete()
        db.session.commit()
        db.session.rollback()

    def empty_table(self) -> None:
        """Function to empty Groups table"""
        Groups.query.delete()
        db.session.commit()

    # def test_member(self) -> None:
    #     """Test that pre-made group has member"""
        
    #     group = Groups.query.first()
        
    #     self.assertEqual(group, self.group)
    #     self.assertEqual(len(group.members), 1)