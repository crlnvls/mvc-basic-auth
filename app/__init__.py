from dotenv import load_dotenv
from os import environ
from flask import Flask, render_template, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager

from .models.user import Users
from .database.db import db
from .routes.main import main_routes

# Load environment variables

load_dotenv()
database_uri = environ.get('DATABASE_URL')
if 'postgres' in database_uri:
    database_uri = database_uri.replace('postgres:', 'postgresql:')

track = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') 
key = environ.get('SECRET_KEY')

# Set up the app 
app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLACHEMY_TRACK_MODIFICATIONS=track,
    SECRET_KEY=key
)

CORS(app)
db.app = app 
migrate = Migrate(app, db)
db.init_app(app)

# Login 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "main.login"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


app.register_blueprint(main_routes)

# Main 

if __name__ == "__main__":
    app.run(debug=True)
