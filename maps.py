import pandas as pd
from app import db
from app.models import Map

data = pd.read_csv('Maps.csv', encoding='utf-8')
for _, row in data.iterrows():
    map = Map()
    map.map_name=row['Map Name']
    map.map_about=row['About']
    db.session.add(map)
db.session.commit()