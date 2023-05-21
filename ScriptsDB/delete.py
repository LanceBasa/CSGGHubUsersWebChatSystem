from app import db
from app.models import Weapon, Rank

def clear_weapons_table():
    Weapon.query.delete()
    db.session.commit()
