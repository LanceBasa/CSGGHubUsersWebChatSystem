import pandas as pd
from app import db
from app.models import Weapon
def populate_weapons_from_csv(filename):
    data = pd.read_csv(filename, encoding='utf-8')
    for _, row in data.iterrows():
        weapon = Weapon.query.filter_by(weapon_name=row['WEAPON']).first()
        if weapon:
            # update existing weapon
            weapon.category = row['CATEGORY']
            weapon.description = row['DESCRIPTION']
        else:
            # create new weapon
            weapon = Weapon(weapon_name=row['WEAPON'], category=row['CATEGORY'], description=row['DESCRIPTION'])
            db.session.add(weapon)
    db.session.commit()

populate_weapons_from_csv('weapons1.csv')     