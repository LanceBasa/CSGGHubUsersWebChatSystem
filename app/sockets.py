from flask import session, request
from app import db, socketio
from app.models import Chat, User,Commands,FavMap,FavWeapon,Map,Weapon,Rank
from flask_socketio import emit, join_room, leave_room
import sys
from sqlalchemy import desc
from flask_login import current_user
from sqlalchemy.orm import joinedload

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


# for adding entered message in the chat to the database and emitting it back to chatbox
@socketio.on("new_message", namespace='/chat')
def handle_new_message(message):
    if current_user.is_authenticated:
        room = session.get("chat")
        
        #strip chat leading and trailing spaces
        message=message.strip()

        # Create a new Chat object and store it in the database
        chat_message = Chat(text=message, user_id=current_user.id)

        db.session.add(chat_message)
        db.session.commit()

        #check if the message is a command if so
        if message[0]=='~':
            print('it is ~')
            comm=message[1:]
            comm=comm.split(" ",1)
            item=""
            if(len(comm)>=2):
                item=comm[1]
                
            command = Commands.query.filter_by(command_name=comm[0]).first()
            if command: 
                comm=eval(command.query_command)
            else:
                comm="command not found"
            emit("chat", {"message": message, "username": current_user.username}, broadcast=True, room=room)
            emit("chat", {"message": comm, "username": 'System'}, broadcast=True, room=room)
        else:
            print(f"New message: {message}", file=sys.stderr)
            emit("chat", {"message": message, "username": current_user.username}, broadcast=True, room=room)
    else:
        print("Error: Unauthenticated user tried to send a message", file=sys.stderr)



#------------- for running special commands---------------------------------

def get_user_fav_weapons(username):
    user = User.query.filter_by(username=username).first()
    if user:
        if user.private==True:
            return username + " has set their profile to private"
        
        user = (Weapon.query
            .join(FavWeapon)
            .filter(FavWeapon.user_id == user.id)
            .with_entities(Weapon.weapon_name)
            .all())
        
        user = sorted(set(fav_weapon.weapon_name for fav_weapon in user))
        user = username+"'s favourite weapons:,"+", ".join(user)
        return user
    return 'Username not found'


def get_all_weapon_names():
    weapon_names = Weapon.query.all()
    weapon_names=sorted(set(weapon.weapon_name for weapon in weapon_names))
    weapon_names = "Weapons List:,\n" + ", ".join(weapon_names)
    return weapon_names



def get_weapons_by_category(category):
    weapons = Weapon.query.filter_by(category=category).all()
    if not weapons:
        weapons = Weapon.query.all()
        weapons = sorted(set(weapon.category for weapon in weapons))
        weapons = "No such class option:," + ",".join(weapons)
        return weapons
    weapons= sorted(set(weapon.weapon_name for weapon in weapons))
    weapons = category + " list:," + ", ".join(weapons)
    return weapons



def get_all_maps():
    maps = Map.query.all()
    maps =sorted(set(map.map_name for map in maps))
    maps = "Maps List:," + ",".join(maps)
    return maps
     

def get_weapon_by_name(name):
    weapon = Weapon.query.filter_by(weapon_name=name).first()
    if weapon:
        text = weapon.description
        text = text.replace(",", "")
        return text
    return "No such weapon found. Please use command, ~weapList, to list all available weapons"



def get_player_rank(name):
    user = User.query.filter_by(username=name).first()
    if user:
        if user.private==True:
            return name + " has set their profile to private"
        
        user=(User.query(Rank.rank_name)
            .join(Rank)
            .filter(Rank.id == user.rank_id)
            .all()
        )
        return user
    return 'Username not found'

def get_user_fav_maps(username):
    user = User.query.filter_by(username=username).first()
    if user:
        if user.private == True:
            return username + " has set their profile to private"
        user = (
            Map.query
            .join(FavMap)
            .filter_by(user_id=user.id)
            .with_entities(Map.map_name)
            .all()
        )
        user = sorted(set(map.map_name for map in user))
        user = username + "'s favourite maps:," + ",".join(user)
        return user
    return 'Username not found'



def get_all_commands():
    commands = Commands.query.all()
    command_names = sorted(set(command.command_name + ":    " + command.command_desc for command in commands))
    command_names = "Here are the commands available:,\n" + ", ".join(command_names)
    return  command_names

def get_map_by_name(name):
    map = Map.query.filter_by(map_name=name).first()
    if map:
        map = map.map_about
        map = map.replace(",", "")
        return map
    return "No such map found. Please use command, ~mapList, to list all available maps"

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