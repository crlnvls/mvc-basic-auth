from dotenv import load_dotenv
from os import environ
from flask import Flask, render_template, request
from flask_cors import CORS

from .database.db import db
from .routes.main import main_routes

# Load environment variables

load_dotenv()
database_uri = environ.get('DATABASE_URL')
track = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') 
key = environ.get('SECRET_KEY')

# Set up the app 
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLACHEMY_TRACK_MODIFICATIONS=track,
    SECRET_KEY=secret_key
)

CORS(app)
db.app = app 
db.init_app(app)

app.register_blueprint(main_routes)

# Main 

if __name__ == "__main__":
    app.run(debug=True)
