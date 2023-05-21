from flask import session, request
from app import db, socketio
from app.models import Chat, User
from flask_socketio import emit, join_room, leave_room
import sys
from sqlalchemy import desc
from flask_login import current_user

from datetime import datetime, timezone

def chat_to_dict(chat):
    return {
        "id": chat.id,
        "text": chat.text,
        "username": chat.author.username,
        "created_at": chat.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"),  # Format the datetime as desired
    }




@socketio.on("new_message", namespace='/chat')
def handle_new_message(message):
    if current_user.is_authenticated:
        room = session.get("chat")
        chat_message = Chat(text=message, user_id=current_user.id)
        db.session.add(chat_message)
        db.session.commit()
        print(f"New message: {message}", file=sys.stderr)
        emit("chat", {
            "message": message,
            "username": current_user.username,
            "created_at": chat_message.created_at.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S')
        }, broadcast=True, room=room)
    else:
        print("Error: Unauthenticated user tried to send a message", file=sys.stderr)

@socketio.on('connect', namespace='/chat')
def handle_connect(data):
    room = session.get("chat")
    join_room(room)
    print('Client connected!', file=sys.stderr)

    messages = Chat.query.order_by(desc(Chat.created_at)).limit(20).all()
    #print(messages)
    messages = [chat_to_dict(msg) for msg in reversed(messages)]  # Use chat_to_dict function
    #print(messages)
    emit('load_messages', messages)

    emit('status', {'msg': 'New client connected!'}, room=room)

@socketio.on('join', namespace='/chat')
def handle_user_join(data):
    room = session.get("chat")
    join_room(room)
    print('Client connected!', file=sys.stderr)

    username = current_user.username  
    join_message = f"User '{username}' has joined the chat"
    emit('chat', {'message': join_message, 'username' :'System'}, room=room, broadcast=True)

@socketio.on("search_message", namespace='/chat')
def handle_search_message(data):
    room = request.sid
    join_room(room)

    search_query = data.get('searchQuery', '').strip()  # Get the search query from the request data
    print(f"Search query: {search_query}", file=sys.stderr)

    if search_query:
        page = data.get('page', 1)  # Retrieve the page number from the request, default to 1 if not provided
        limit = 10  # Number of items per page
        offset = (page - 1) * limit  # Calculate the offset

        # Perform the database query to retrieve matching messages with pagination
        messages = (
            db.session.query(Chat)
            .filter(Chat.text.like(f'%{search_query}%'))
            .limit(limit)
            .offset(offset)
            .all()
        )
        print(f"Search results: {messages}", file=sys.stderr)

        search_results = [chat_to_dict(message) for message in messages]
        emit("search_results", search_results)
    else:
        # If the search query is empty, send an empty list as search results
        emit("search_results", [])
