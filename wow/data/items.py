import json

with open("wow/data/items.json", "r") as in_file:
    wow_items = json.load(in_file)

item_sets = {item: set(item) for item in wow_items}
