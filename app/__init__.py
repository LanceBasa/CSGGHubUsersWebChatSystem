from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO

# Create a Flask application
app = Flask(__name__)
# Load configuration from Config class
app.config.from_object(Config)
# Initialize the SQLAlchemy database
db = SQLAlchemy(app)
 # Initialize the Flask-Migrate extension
migrate = Migrate(app, db)
# Initialize the Flask-Login extension
login = LoginManager(app)
login.login_view = 'login'  # Set the login view for authentication
app.config['SECRET_KEY'] = 'your_secret_key'  # Set a secret key for session encryption
# Initialize the Flask-SocketIO extension
socketio = SocketIO(app)


#if __name__ == '__main__':
#    socketio.run(app)

# Import routes, models, and sockets from the app module
from app import routes, models, sockets