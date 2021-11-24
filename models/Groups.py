from models.main import db
from sqlalchemy.sql.functions import now
from models.Group_Payments import Group_Payments

class Groups(db.Model):
    __tablename__ = "groups"

    id = db.Column(
        db.Integer(),
        primary_key=True,
        autoincrement=True,
        unique=True
    )
    
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    
    name = db.Column(
        db.String(30),
        nullable=False
    )

    description = db.Column(
        db.String(200),
        nullable=True
    )
    
    created_on = db.Column(
        db.DateTime(timezone=True),
        default=now()
    )

    # user = db.relationship("Users", backref="group_user", passive_deletes=True)
    members = db.relationship("Group_Members", backref="group", passive_deletes=True)
    payments = db.relationship("Group_Payments", backref="group")
    def __repr__(self):
        return f'<Groups id={self.id} user_id={self.user_id} name={self.name} description={self.description} created_on={self.created_on}>'