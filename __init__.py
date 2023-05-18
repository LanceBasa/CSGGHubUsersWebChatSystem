from flask import Flask, Blueprint
from app import app
from app.auth import routes
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap




app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)
bp = Blueprint('errors', __name__)
from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app import models

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    if not app.debug and not app.testing:
        return app

