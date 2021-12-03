from flask_sqlalchemy import SQLAlchemy
from typing import TYPE_CHECKING

db = SQLAlchemy()
BaseModel = None

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model

    BaseModel = db.make_declarative_base(Model)
else:
    BaseModel = db.Model
    
def connect_db(app):
    db.app = app
    db.init_app(app)
