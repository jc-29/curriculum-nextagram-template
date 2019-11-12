import os
import config
from flask import Flask
from models.base_model import db
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from models.user import User_

login_manager = LoginManager()


web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
csrf = CSRFProtect(app)
login_manager.init_app(app)
login_manager.login_view = 'sessions.new'
login_manager.login_message = 'Please login before proceeding...'
login_manager.login_message_category = "warning"


if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

@login_manager.user_loader
def load_user(user_id):
    return User_.get_or_none(id= user_id)