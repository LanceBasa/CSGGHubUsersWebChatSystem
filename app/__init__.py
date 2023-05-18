from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
app.config['SECRET_KEY'] = 'your_secret_key'  # Set a secret key for session encryption
socketio = SocketIO(app)


#if __name__ == '__main__':
#    socketio.run(app)
from app import routes, models, sockets