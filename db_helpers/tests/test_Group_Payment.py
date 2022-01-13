"""Unit test for Group_Payment class"""

import sys

sys.path.append("../..")

from unittest import TestCase
from app import app, connect_db, db
from models.Group_Payments import Group_Payments
from models.Group_Members import Group_Members
from models.Users import Users
from models.Member_Payments import Member_Payments
from db_helpers.Group_Payment import Group_Payment
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

class Group_PaymentTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        """Create user and group"""
        Users.query.delete()
        
        cls.user: User = User.sign_up(**demo_user_json)
        cls.group: Group = cls.user.make_group("New group!", "I made a group!")
        
        return super().setUpClass()
    
    def setUp(self) -> None:
        """Create Group_Payment"""
        Group_Payments.query.delete()
        self.group_payment = self.group.add_payment("PAYMNT", 332)
    
    def tearDown(self) -> None:
        """Rollback session"""
        db.session.rollback()
    
    def test_group_payment(self):
        """Test that group payment exists in database"""
        group_payment_from_db: Group_Payments = Group_Payments.query.get(self.group_payment.key)

        self.assertEqual(group_payment_from_db.id, self.group_payment.id,
                         "Test that id of member_payment is the same from the database and object")
    
    def test_get_by_id(self) -> None:
        """Test get_by_id method"""
        group_payment = Group_Payment.get_by_id(self.group_payment.id, self.group_payment.group_id)
        
        self.assertEqual(group_payment.id, self.group_payment.id,
                         "Test that group payment's id from get_by_id is the same as group_payment's id")
    
    def test_edit(self) -> None:
        """Test edit method"""
        self.group_payment.edit("EDITED", 80)
        group_payment_from_db: Group_Payments = Group_Payments.query.get(self.group_payment.key)
        
        self.assertEqual(self.group_payment.total_amount, 80, "Test that group_payment amount is changed")
        self.assertEqual(group_payment_from_db.id, self.group_payment.id,
                         "Test that group_payment amount changed in database and object")
    
    def test_delete(self) -> None:
        """Test delete method"""
        self.group_payment.delete()
        group_payment_from_db: Group_Payments = Group_Payments.query.filter_by(id=self.group_payment.id, group_id=self.group.id).first()

        self.assertEqual(group_payment_from_db, None, "Test that member_payment cannot be found in database")