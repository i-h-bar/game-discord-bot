import json
from collections import defaultdict

from cache import AsyncLRU

with open("wow/data/items.json") as in_json:
    wow_items = json.load(in_json)


@AsyncLRU()
async def item_starting_letters() -> dict[str, set[str]]:
    return {item: set(word[:2] for word in item.split()) for item in wow_items}


@AsyncLRU()
async def starting_letter_groups() -> dict[str, list[str]]:
    letter_groups = defaultdict(list)

    for item, starting_letters in (await item_starting_letters()).items():
        for starting_letter in starting_letters:
            letter_groups[starting_letter].append(item)

    return letter_groups
