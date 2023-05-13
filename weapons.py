import csv

def print_weapons_from_csv(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            weapon_name, category = row
            print(f"Weapon Name: {weapon_name}, Category: {category}")

print_weapons_from_csv('weapons.csv')