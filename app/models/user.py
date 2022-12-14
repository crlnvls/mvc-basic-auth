from ..database.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    # Check hash with password 

    @property
    def password_hash(self):
	    raise AttributeError('password is not a readable attribute!')

    @password_hash.setter
    def password_hash(self, password):
	    self.password_hash = generate_password_hash(password)

    def verify_password_hash(self, password):
	    return check_password_hash(self.password_hash, password)

    # Validate if user exists

    def validate_username(self, username):
            existing_user_username = User.query.filter_by(
                username=username.data).first()
            if existing_user_username:
                raise ValidationError(
                    'That username already exists. Please choose a different one.')

    
