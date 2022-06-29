import json

with open("wow/data/items.json", "r") as in_file:
    wow_items = json.load(in_file)


wow_item_names = list(wow_items.keys())
