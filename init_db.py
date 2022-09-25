from app import db
from app.models.user import Users 

db.drop_all()
db.create_all()
