import os # Import the os module for working with operating system functionalities

# Get the base directory path of the application
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    # Set the SECRET_KEY for the application. It is obtained from the environment variable 'SECRET_KEY'.
    # If the environment variable is not set, a default value ('your_secret_key_here') is used.
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # Set the URI for the database. It is obtained from the environment variable 'DATABASE_URL'.
    # If the environment variable is not set, a SQLite database file path is used based on the 'app.db' file
    # located in the 'basedir' directory.

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Disable modification tracking for SQLAlchemy. Setting it to 'False' improves performance.
