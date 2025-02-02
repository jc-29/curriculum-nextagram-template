from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.user import User_

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")


# @login_manager.user_loader
# def load_user(user_id):
#     return User_.get(user_id)

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def item_not_found_error(e):
    return render_template('404.html'), 404


@app.route("/")
def home():
    return render_template('home.html')
