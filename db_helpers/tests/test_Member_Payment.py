"""Unit test for Member_Payment class"""

import sys

from db_helpers.Member_Payment import Member_Payment

sys.path.append("../..")

from unittest import TestCase
from app import app, connect_db, db
from models.Group_Members import Group_Members
from models.Users import Users
from models.Member_Payments import Member_Payments
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
# User -> Group -> Group_Payment
#               -> Group_Member -> Member_Payment

class Member_PaymentTestCase(TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Create user, group, group payment, and group member"""
        Users.query.delete()
        
        cls.user: User = User.sign_up(**demo_user_json)
        cls.group: Group = cls.user.make_group("New group!", "I made a group!")
        cls.group_payment = cls.group.add_payment("Hello!", 323)
        cls.group_member = cls.group.add_member("Memb3r", "membr@membr.com", "2312313132")
        
        return super().setUpClass()
    
    def setUp(self) -> None:
        """Create Member_Payment"""
        Member_Payments.query.delete()
        self.member_payment = self.group_member.add_payment(self.group_payment.id, 21)
    
    def tearDown(self) -> None:
        """Rollback session"""
        db.session.rollback()
    
    def test_member_payment(self):
        """Test that member payment exists in database"""
        member_payment_from_db: Member_Payments = Member_Payments.query.get(
            (self.group_member.id, 
            self.group_payment.id)
        )

        self.assertEqual((member_payment_from_db.member_id, member_payment_from_db.group_payment_id),
                         (self.group_member.id, self.group_payment.id),
                         "Test that id of member_payment is the same from the database and object")
    
    def test_get_by_id(self) -> None:
        """Test get_by_id method"""
        member_payment = Member_Payment.get_by_id(self.member_payment.member_id, self.member_payment.group_payment_id)
        
        self.assertEqual((member_payment.member_id, member_payment.group_payment_id),
                         (self.group_member.id, self.group_payment.id),
                         "Test that member payment's id from get_by_id is the same as member_payment's id")