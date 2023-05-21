from app import app, db, socketio # Import the Flask application instance, database instance, and SocketIO instance
from app.models import User, Chat # Import the User and Chat models

@app.shell_context_processor
def make_shell_context():
    # Define a shell context processor that adds the 'db', 'User', and 'Chat' variables to the shell context
    return {'db': db, 'User': User, 'Chat': Chat}

if __name__ == '__main__':
    socketio.run(app)
    # If the current module is being executed as the main script (not imported),
    # run the Flask application using the SocketIO server provided by the 'socketio' module.