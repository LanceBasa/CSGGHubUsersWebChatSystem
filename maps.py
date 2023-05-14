from app import db
from app.models import Map

def add_maps_from_txt(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            map_name = line.strip() # Remove newline character
            map = Map(map_name=map_name)
            db.session.add(map)
    db.session.commit()

add_maps_from_txt('Maps.txt')