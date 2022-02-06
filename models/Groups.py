from models.Group_Members import Group_Members
from models.Group_Payments import Group_Payments
from models.main import db, BaseModel
from sqlalchemy.sql.functions import now
from dataclasses import dataclass

@dataclass
class Groups(BaseModel):
    __tablename__ = "groups"

    id: int = db.Column(
        db.Integer(),
        primary_key=True,
        autoincrement=True,
        unique=True,
        index=True
    )
    
    user_id: int = db.Column(
        db.Integer(),
        db.ForeignKey("users.id", ondelete="CASCADE"),
    )
    
    name: str = db.Column(
        db.String(30),
        nullable=False
    )

    description: str = db.Column(
        db.String(200),
        nullable=True
    )
    
    created_on = db.Column(
        db.DateTime(timezone=True),
        default=now()
    )

    # user = db.relationship("Users", backref="group_user", passive_deletes=True)
    members: Group_Members = db.relationship("Group_Members", backref="group", passive_deletes=True)
    payments: Group_Payments = db.relationship("Group_Payments", backref="group")
    
    def __repr__(self):
        return f'<Groups id={self.id} user_id={self.user_id} name={self.name} description={self.description} created_on={self.created_on} members={self.members}>'