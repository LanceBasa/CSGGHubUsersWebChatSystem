from app import db
from app.models import Weapon

def clear_weapons_table():
    Weapon.query.delete()
    db.session.commit()
