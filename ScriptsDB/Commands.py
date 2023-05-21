import pandas as pd # Import the pandas library for working with data frames
from app import db # Import the Flask SQLAlchemy database instance
from app.models import Commands # Import the Commands model from the app.models module

# Read the CSV file into a pandas DataFrame
data = pd.read_csv('Commands2.csv', encoding='utf-8')
# Iterate over each row in the DataFrame
for _, row in data.iterrows():
    # Create a new instance of the Commands model
    command = Commands()

    # Assign values from the DataFrame row to the model attributes
    command.command_name=row['name']
    command.command_desc=row['description']
    command.query_command=row['command']
    
    # Add the command object to the database session
    db.session.add(command)
    # Commit the changes to the database
    
db.session.commit()