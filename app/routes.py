from flask import render_template, flash, redirect, url_for, Blueprint
from app import app,SocketIO
from app.forms import LoginForm, EditProfileForm
from flask_login import logout_user, current_user, login_user, login_required
from app.models import User
from datetime import datetime
from app.models import User,Map, FavMap, Weapon, FavWeapon, Commands, Chat
from flask_socketio import SocketIO, emit
from sqlalchemy import or_

#libraries to redirect a non-logged in user back to the login page when they tries
#to access the protected index page
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm

# Importing necessary modules and packages

@app.route('/')
def homePage():
    return render_template("homePage.html", title='Welcome to CSGGHub')

@app.route('/chat', methods=['POST','GET']) 
@login_required
def chat():
    return render_template("chat.html", title='Chatroom - CSGGHub')

@app.route('/profile/<username>')
#making sure a user is logged in to access the index page '@login_required'
@login_required 
def profile(username):
    user=User.query.filter_by(username=current_user.username).first_or_404()

    # if the viewer is another person
    if (current_user.username !=username):
        anotherUser=User.query.filter_by(username=username).first_or_404()
        #check if its private if it is, return to the logged in profile
        # if not view the user profile
        if anotherUser.private:
            flash(f"User '{username}' has set their profile to private. You have been redirected to your profile")

        else:
            return render_template("profile.html", title='My Profile', user=anotherUser)
    return render_template("profile.html", title='My Profile', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('profile', username=current_user.username)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homePage'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    form.fav_maps.choices = [(map.id, map.map_name) for map in Map.query.order_by(Map.map_name)]
    form.fav_weapons.choices = [(weapon.id, weapon.weapon_name) for weapon in Weapon.query.order_by(Weapon.weapon_name)]
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.id != current_user.id: 
            flash('Username already in use, please choose a different one.')
            return redirect(url_for('edit_profile')) # redirect back to 'edit_profile'
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.private= form.isPrivate.data
        fav_map_ids = request.form.getlist('fav_maps')
        fav_weapon_ids = request.form.getlist('fav_weapons')

        # Clear all favorite maps
        for fav_map in current_user.fav_maps.all():
            current_user.fav_maps.remove(fav_map)

        # Clear all favorite weapons
        FavWeapon.query.filter_by(user_id=current_user.id).delete()

        # Add the selected maps
        for map_id in fav_map_ids:
            map = Map.query.get(map_id)
            if map:
                fav_map = FavMap(user=current_user, map=map)
                db.session.add(fav_map)

        # Add the selected weapons
        for weapon_id in fav_weapon_ids:
            weapon = Weapon.query.get(weapon_id)
            if weapon:
                fav_weapon = FavWeapon(user_id=current_user.id, weapon_id=weapon_id)
                db.session.add(fav_weapon)

        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile', username=current_user.username))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.fav_maps.data = [fav_map.map_id for fav_map in current_user.fav_maps]
        form.fav_weapons.data = [fav_weapon.weapon_id for fav_weapon in FavWeapon.query.filter_by(user_id=current_user.id)]

    return render_template('edit_profile.html', title='Edit Profile', form=form)


#------- for special commands-----------------
def get_user_fav_weapons(username):
    user = User.query.filter_by(username=username).first()
    if user:
        fav_weapons = (
            FavWeapon.query
            .join(Weapon)
            .options(joinedload(FavWeapon.weapon))
            .filter_by(user_id=user.id)
            .all()
        )
        return [fav_weapon.weapon.weapon_name for fav_weapon in fav_weapons]
    return 'Username not found'

def get_all_weapon_names():
    weapon_names = Weapon.query.with_entities(Weapon.name).all()
    return [name for (name,) in weapon_names]

def get_weapons_by_category(category):
    weapons = Weapon.query.filter_by(category=category).all()
    return weapons

def get_all_maps():
    maps = Map.query.all()
    return maps

def get_weapon_by_name(name):
    weapon = Weapon.query.filter_by(weapon_name=name).first()
    if weapon:
        text = weapon.description
        return text
    return "No such weapon found"

def get_player_rank(name):
    users = User.query.filter_by(username=name).first()
    return users

def get_user_fav_maps(username):
    user = User.query.filter_by(username=username).first()
    if user:
        fav_maps = (
            FavMap.query
            .join(Map)
            .options(joinedload(FavMap.map))
            .filter_by(user_id=user.id)
            .all()
        )
        return [fav_map.map.map_name for fav_map in fav_maps]
    return 'Username not found'

def get_all_commands():
    commands = Commands.query.with_entities(Commands.name).all()
