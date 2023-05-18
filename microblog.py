from app import app, db, socketio
from app.models import User, Chat

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Chat': Chat}

if __name__ == '__main__':
    socketio.run(app)