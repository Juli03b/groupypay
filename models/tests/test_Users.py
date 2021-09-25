# from unittest import TestCase
# from Users import Users
# from app import app, connect_db, db

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///groupypay_test'
# app.config['SQLALCHEMY_ECHO'] = False

# connect_db(app)

# db.drop_all()
# db.create_all()

# class UserTestCase(TestCase):
#     def setUp(self) -> None:
#         Users.query.delete()
#         db.session.commit()
        
#         self.user_password = "123TESTING"
#         self.user_username = "THISISATEST"
#         self.user = Users.signup(
#             username=self.user_username, 
#             password=self.user_password, 
#             first_name="TEST",
#             last_name="TESTING",
#             email="test@test.com",
#             phone_number="221313132")

#         db.session.add(self.user)
#         db.session.commit()

#         self.user_id = self.user.id
    
#     def tearDown(self) -> None:
#         db.session.rollback()
    
#     def getUser(self) -> None:
#         print(self.user)