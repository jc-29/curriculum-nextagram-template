from flask import Blueprint, render_template, redirect, request,url_for, flash
from werkzeug.security import generate_password_hash
from models.user import User_
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash



users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    email=request.form.get('email')
    password=request.form.get('password')
    hash_password = generate_password_hash(password)
    x = User_(username=username, email=email, password=hash_password)
    if x.save():
        flash('Successfully signed up!',"success")
        return redirect(url_for('sessions.new'))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id_>/edit', methods=['GET'])
def edit(id_):
    # user = User_.get_or_none(User_.id == id_)
    if current_user.is_authenticated:
        if int(current_user.id) == int(id_) :
            return render_template('users/edit_form.html', id_=id_)
        else:
            return 'oops'
    else:
        flash('Error! Please sign in!', 'danger')
        return redirect(url_for('sessions.new'))
    

@users_blueprint.route('/<id_>', methods=['POST'])
def update(id_):
    username = request.form.get('current-username')
    email = request.form.get('current-email')
    password = request.form.get('current-password') 
    user = User_.get(User_.id == id_)
    user.username = username
    user.email = email
    print(user)
    if user.save():
        flash('Successfully Updated!', 'success')
        return redirect(url_for('users.edit',id_=id_))
    else:
        flash('Error', 'danger')
        return render_template('/users/edit.html',id_=id_)
        
    if check_password_hash(user.password, password):


