import pandas as pd
from app import db
from app.models import Commands

data = pd.read_csv('Commands2.csv', encoding='utf-8')
for _, row in data.iterrows():
    command = Commands()
    command.command_name=row['name']
    command.query_command=row['command']
    db.session.add(command)
db.session.commit()