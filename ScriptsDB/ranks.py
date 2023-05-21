from app import db
from app.models import Rank

def add_maps_from_txt(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            rank_name = line.strip() # Remove newline character
            rank = Rank(rank_name=rank_name)
            db.session.add(rank)
    db.session.commit()

add_maps_from_txt('Ranks.txt')