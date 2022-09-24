from app import db
from apps.models.app import App 

db.drop_all()
db.create_all()
