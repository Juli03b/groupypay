from unittest import TestCase
from app import app, connect_db, db
from models.Users import Users

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///groupypay_test'
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    def setUp(self) -> None:
        """Empty Users table and create a new user"""
        Users.query.delete()
        db.session.commit()
        
        self.user_password = "123TESTING"
        self.user_username = "THISISATEST"
        self.user = Users.sign_up(
            first_name="TEST",
            last_name="TESTING",
            email="test@test.com",
            password=self.user_password, 
            phone_number="+1 213 999 2332"
        )

        db.session.add(self.user)
        db.session.commit()

        self.user_id = self.user.id
    
    def tearDown(self) -> None:
        db.session.rollback()

    def empty_table(self) -> None:
        """Function to empty Users table"""
        Users.query.delete()
        db.session.commit()

    def test_user(self) -> None:
        """Test that pre-made user can be found"""
        user = Users.query.first()
        self.assertEqual(user, self.user)
    
    def test_sign_up(self) -> None:
        """Create a new user, then query it and test for equality"""

        self.empty_table()

        # Create new user
        new_user = Users.sign_up(
            first_name="SIR",
            last_name="TESTING",
            email="testIT@test.com",
            password=self.user_password, 
            phone_number="+13221239681"
        )

        # Add and commit to db
        db.session.add(new_user), db.session.commit()

        # Query for new_user
        user_query = Users.query.first()

        self.assertEqual(new_user, user_query, "Test that both user instances are the same")
        self.assertEqual(new_user.password[0:7], "$2b$12$", "Test that password is Bcrypy encrypted")
        