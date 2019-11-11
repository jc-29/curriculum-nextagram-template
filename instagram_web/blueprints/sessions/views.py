from flask import Blueprint, render_template, redirect, request,url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User_
from flask_login import login_user,logout_user, current_user


sessions_blueprint = Blueprint('sessions', __name__, template_folder='templates')

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    logout_user()
    return render_template('sessions/new.html')

@sessions_blueprint.route('/', methods=['POST'])
def login():
    username = request.form.get('username')
    entered_password = request.form.get('password')
    look_for_user = User_.get_or_none(User_.username==username)
    if look_for_user:
        user_password = look_for_user.password
        result = check_password_hash(user_password, entered_password)
        if result:
            login_user(look_for_user)
            flash('Successfully logged in!', 'success')
            return render_template('home.html')
        else:
            flash('Login failed! Password incorrect', 'danger')
            return redirect(url_for('sessions.new'))
    else: 
        flash('Login failed! No user with that username', 'danger')
        return redirect(url_for('sessions.new'))

