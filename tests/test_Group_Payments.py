"""Unit test for Groups_Payments model"""

import sys

sys.path.append("..")

from unittest import TestCase
from app import app, connect_db, db
from models.Users import Users
from models.Groups import Groups
from models.Group_Payments import Group_Payments

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///groupypay_test'
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)

db.drop_all(), db.create_all()

class Group_PaymentsTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Create new user to create groups with"""
        Users.query.delete()
        
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
        """Empty Groups table and create a new group, and add a payment"""
        # Create group
        self.group = Groups(
            name="TEST TESTING",
            user_id=self.user_id,
            description="TESTSTSETTSE"
        )

        db.session.add(self.group)
        db.session.commit()

        self.group_id = self.group.id
        
        # Create Payment
        self.payment = Group_Payments(
            name="f00d",
            total_amount=31.323,
        )
        
        self.group.payments.append(self.payment)
        db.session.commit()
    
    def tearDown(self) -> None:
        Groups.query.delete()
        db.session.commit()
        db.session.rollback()

    def empty_table(self) -> None:
        """Empty Groups table"""
        Groups.query.delete()
        db.session.commit()

    def test_group(self) -> None:
        """Test that pre-made group can be found"""
        group = Groups.query.first()

        self.assertEqual(group, self.group)
        
    def test_group_payment(self) -> None:
        """Test that group payment can be found"""
        self.assertEqual(len(self.group.payments), 1)