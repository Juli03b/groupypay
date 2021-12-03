from models.main import db, BaseModel
from sqlalchemy.sql.functions import now

class Group_Members(BaseModel):
    __tablename__ = "group_members"

    id: int = db.Column(
        db.Integer(), 
        primary_key=True, 
        autoincrement=True,
        unique=True
    )
    group_id: int = db.Column(
        db.Integer(),
        db.ForeignKey("groups.id", ondelete="CASCADE"),
        primary_key=True
    )
    name: str = db.Column(
        db.String(55),
        nullable=False
    )
    email: str = db.Column(
        db.String(127),
        nullable=False
    )
    phone_number: str = db.Column(
        db.String(),
        nullable=True,
    )
    added_on = db.Column(
        db.DateTime(timezone=True),
        default=now()
    )

    payments = db.relationship("Member_Payments", backref="group_member", passive_deletes=True)

    def __repr__(self):
        return f'<Group_Members id={self.id} group_id={self.group_id} name={self.name} email={self.email} phone_number={self.phone_number} added_on={self.added_on}>'