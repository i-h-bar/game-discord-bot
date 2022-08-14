import json
from collections import defaultdict

with open("wow/data/items.json") as in_json:
    wow_items = json.load(in_json)

item_starting_letters = {item: set(word[:2] for word in item.split()) for item in wow_items}

starting_letter_groups = defaultdict(list)

for item, starting_letters in item_starting_letters.items():
    for starting_letter in starting_letters:
        starting_letter_groups[starting_letter].append(item)
