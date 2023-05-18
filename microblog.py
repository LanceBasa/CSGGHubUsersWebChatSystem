from app import app, db
from app.models import User, Chat
import eventlet

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Chat': Chat}

if __name__ == '__main__':
    eventlet.monkey_patch()  # Apply Eventlet's monkey patching
    app.run(threaded=True)  # Use the Eventlet server with threaded mode enabled