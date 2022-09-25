from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from ..database.db import db
from ..models.user import Users

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo 

from werkzeug.security import generate_password_hash, check_password_hash

main_routes = Blueprint("main", __name__)


# Forms

class RegisterForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    email= StringField(validators=[
        InputRequired()], render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})


    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

# Routes

@main_routes.route("/", methods=['GET'])
def home():
    return "<h1>Hello!</h1>"

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main.dashboard'))
    return render_template('login.html', form=form)

@main_routes.route('/dashboard',  methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_routes.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = Users.query.filter_by(email=form.email.data).first()
        username = Users.query.filter_by(username=form.username.data).first()
        if email is not None:
            return "<h1>Email already exist</h1>"
        elif username is not None:
            return "<h1>Username already exist</h1>"
        else:
            hashed_password = generate_password_hash(form.password.data)
            new_user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.login'))

    return render_template('register.html', form=form)
