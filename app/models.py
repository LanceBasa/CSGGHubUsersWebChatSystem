from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

# User loader function for Flask-Login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    # User model representing the user table in the database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    rank_id = db.Column(db.Integer, db.ForeignKey('rank.id'))
    private = db.Column(db.Boolean, default=False)
    chat = db.relationship('Chat', backref='author', lazy='dynamic')
    fav_weapons = db.relationship('FavWeapon', backref='user', lazy='dynamic')
    fav_maps = db.relationship('FavMap', backref='user', lazy='dynamic')
    about_me = db.Column(db.String(300))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    

class Chat(db.Model):
    # Chat model representing the chat table in the database
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<Chat {}>'.format(self.text)


class FavWeapon(db.Model):
    # FavWeapon model representing the many-to-many relationship between users and favorite weapons
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    weapon_id = db.Column(db.Integer, db.ForeignKey('weapon.id'))

    def __repr__(self):
        return '<FavWeapon {}>'.format(self.id)

class Weapon(db.Model):
    # Weapon model representing the weapon table in the database
    id = db.Column(db.Integer, primary_key=True)
    weapon_name = db.Column(db.String(64), unique=True)
    category = db.Column(db.String(64))
    description = db.Column(db.String(500))
    users = db.relationship('FavWeapon', backref='weapon', lazy='dynamic')

    def __repr__(self):
        return '<Weapon {}>'.format(self.weapon_name)

class FavMap(db.Model):
    # FavMap model representing the many-to-many relationship between users and favorite maps
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    map_id = db.Column(db.Integer, db.ForeignKey('map.id'))

    def __repr__(self):
        return '<FavMap {}>'.format(self.id)

class Map(db.Model):
    # Map model representing the map table in the database
    id = db.Column(db.Integer, primary_key=True)
    map_name = db.Column(db.String(64), unique=True)
    map_about = db.Column(db.String(500))
    users = db.relationship('FavMap', backref='map', lazy='dynamic')

    def __repr__(self):
        return '<Map {}>'.format(self.map_name)

class Rank(db.Model):
    # Rank model representing the rank table in the database
    id = db.Column(db.Integer, primary_key=True)
    rank_name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='rank', lazy='dynamic')

    def __repr__(self):
        return '<Rank {}>'.format(self.rank_name)
    
    
class Commands(db.Model):
    # Commands model representing the commands table in the database
    id = db.Column(db.Integer, primary_key=True)
    command_name = db.Column(db.String(16), unique=True)
    command_desc = db.Column(db.String(64))
    query_command = db.Column(db.String(64))

    def __repr__(self):
        return '<Commands {}>'.format(self.command_name)