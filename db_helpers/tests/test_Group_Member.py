"""Unit test for Group_Member class"""

import sys

sys.path.append("../..")

from unittest import TestCase
from app import app, connect_db, db
from models.Group_Members import Group_Members
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

class Group_MemberTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        """Create user and group"""
        cls.user: User = User.sign_up(**demo_user_json)
        cls.group: Group = cls.user.make_group("New group!", "I made a group!")
        
        return super().setUpClass()

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
        """Test edit method"""
        self.group_member.edit("0iluj", "011uJ@gmail.com", "322718713")
        group_member_from_db: Group_Members = Group_Members.query.filter_by(id=self.group_member.id).first()
        
        self.assertEqual(self.group_member.name, group_member_from_db.name, "Test that name changes in both group_member object and in db")

    def test_add_payment(self) -> None:
        """Test add_payment mehtod"""
        group_payment = self.group.add_payment("Payment!!!", 9999999)
        member_payment = self.group_member.add_payment(group_payment.id, 31323.331)
        member_payment_from_db: Member_Payments = Member_Payments.query.filter_by(
            member_id=member_payment.member_id,
            group_payment_id=member_payment.group_payment_id
        ).first()
        
        self.assertEqual((member_payment.member_id, member_payment.group_payment_id), 
                         (member_payment_from_db.member_id, member_payment_from_db.group_payment_id),
                         "Test that member payment can be found in db")