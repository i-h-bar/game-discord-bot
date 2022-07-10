import json

with open("wow/data/items.json", "r") as in_file:
    wow_items = json.load(in_file)


with open("wow/data/extra_item_info.json") as in_file:
    wow_items_extra = json.load(in_file)

item_starting_letters = {item: set(word[:2] for word in item.split()) for item in wow_items}
