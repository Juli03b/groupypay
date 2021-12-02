"""Unit test for User class"""
# TEST EDIT!!!!!!!!!!!!!!
import sys


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

class GroupTestCase(TestCase):
    
    def setUp(self) -> None:
        """Create user and group"""
        Users.query.delete()
        db.session.commit()
        
        self.user: User = User.sign_up(**demo_user_json)
        self.group: Group = self.user.make_group("New group!", "I made a group!")

    def tearDown(self) -> None:
        """Rollback session"""
        
        db.session.rollback()
    
    def test_group(self) -> None:
        """Test if group exists"""
        group_from_db: Groups = Groups.query.filter_by(id=self.group.id).first()

        self.assertEqual(group_from_db.id, self.group.id)
        
    def test_get_by_id(self) -> None:
        """Test get_by_id method"""
        group = Group.get_by_id(self.group.id)
        
        self.assertEqual(group.id, self.user.id)
        
    def test_add_payment(self) -> None:
        """Test add_payment"""
        payment = self.group.add_payment("Games", 132.322)
        payment_from_db: Group_Payments = Group_Payments.query.filter_by(id=payment.id).first()
        
        self.assertEqual(payment.id, payment_from_db.id, "Test that payment can be found in db")
    
    def test_add_member(self) -> None:
        """Test add_member"""
        member = self.group.add_member("Julio2.0", "JB2@gmail.com", "3132233")
        member_from_db: Group_Members = Group_Members.query.filter_by(id=member.id).first()
        
        self.assertEqual(member.id, member_from_db.id, "Test that member can be found in db")