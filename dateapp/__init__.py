from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dateapp.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from dateapp.users.routes import users
    from dateapp.likes.routes import likes
    from dateapp.messagess.routes import messagess
    from dateapp.matches.routes import matches
    from dateapp.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(likes)
    app.register_blueprint(messagess)
    app.register_blueprint(matches)
    app.register_blueprint(main)

    return app