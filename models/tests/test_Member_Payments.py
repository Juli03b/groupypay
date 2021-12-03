"""Unit test for Member_Payments model"""

import sys

sys.path.append("../..")

from unittest import TestCase
from app import app, connect_db, db
from models.Users import Users
from models.Groups import Groups
from models.Group_Payments import Group_Payments
from models.Group_Members import Group_Members
from models.Member_Payments import Member_Payments

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///groupypay_test'
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)

db.drop_all(), db.create_all()

class Member_PaymentsTestCase(TestCase):
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
        """Empty Groups table and create a new group"""
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
        
        self.payment_id = self.payment.id
        
        # Add member to group
        self.member = Group_Members(
            name="TEEEST",
            email="TESTINGTON@TEST.com",
            phone_number="+132312323"
        )
        self.group.members.append(self.member)
        
        db.session.commit()
        
        self.member_id = self.member.id
        
        # Create member payment
        self.member_payment = Member_Payments(
            member_id=self.member_id,
            group_payment_id=self.payment_id,
            amount=12
        )
        self.payment.member_payments.append(self.member_payment)
        
        db.session.commit()
        
    def tearDown(self) -> None:
        Groups.query.delete()
        db.session.commit()
        db.session.rollback()

    def empty_table(self) -> None:
        """Empty Groups table"""
        Groups.query.delete()
        db.session.commit()

    def test_member_payment(self) -> None:
        """Test that pre-made member payment can be found"""
        self.assertTrue(self.member_payment)