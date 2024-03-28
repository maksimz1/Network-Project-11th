import json

with open('Weapons.json') as f:
	data = json.load(f)
	print(data['weapons']['M4A1'])