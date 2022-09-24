from app import db
from app.models.user import User 

db.drop_all()
db.create_all()
