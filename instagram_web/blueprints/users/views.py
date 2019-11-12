from flask import Blueprint, render_template, redirect, request,url_for, flash
from werkzeug.security import generate_password_hash
from models.user import User_
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from instagram_web.util.helpers import upload_file_to_s3
from werkzeug.utils import secure_filename
from config import Config



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
    else: 
        for error in x.errors:
            flash(error, 'danger')
        return redirect(url_for('users.new'))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id_>/edit', methods=['GET'])
@login_required
def edit(id_):
    # user = User_.get_or_none(User_.id == id_)
    
    if int(current_user.id) == int(id_) :
        return render_template('users/edit_form.html', id_=id_)
    else:
        flash('Invalid action!', 'danger') #for when user is signed in but tries to access another account's edit page
        return redirect(url_for('home'))
    
    

@users_blueprint.route('/<id_>', methods=['POST'])
@login_required
def update(id_):
    password = request.form.get('current-password') 
    user = User_.get(User_.id == id_)

    if check_password_hash(user.password, password):
        username = request.form.get('current-username')
        email = request.form.get('current-email')
        user.username = username
        user.email = email
        if user.save():
            flash('Successfully Updated!', 'success')
            return redirect(url_for('users.edit',id_=id_))
        else:
            for error in user.errors:
                flash(error, 'danger')
            return render_template('users/edit_form.html',id_=id_)
    else:
        flash('Invalid Password!', 'danger')
        return redirect(url_for('users.edit',id_=id_))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@users_blueprint.route('/<id_>/picture', methods=['POST'])
@login_required
def update_picture(id_):
    file_to_upload = request.files['user_file']
    
    if not file_to_upload:
        flash('Please choose a file to upload', 'danger')
        return redirect(url_for('users.edit', id_=id_))

    elif file_to_upload and allowed_file(file_to_upload.filename): 
        file_to_upload.filename = secure_filename(file_to_upload.filename)
        output = upload_file_to_s3(file_to_upload)
        x = (User_.update({User_.profile_picture: output}).where(User_.id == current_user.id))
        x.execute()
        flash('Profile picture updated successfully!', 'success')
        return redirect(url_for('users.edit', id_=id_))
    else:
        flash('Inavlid file type!','danger')
        return redirect(url_for('users.edit', id_=id_))
    


