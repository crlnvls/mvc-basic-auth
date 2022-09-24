from flask import Blueprint, request, render_template
from ..database.db import db
from ..models.app import App

main_routes = Blueprint("main", __name__)

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
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@main_routes.route('/dashboard',  methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_routes.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)
