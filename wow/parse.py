import re
import json

from functools import lru_cache
from utility_functions.levenshtein import levenshtein_distance

with open("wow/data/items.json", "r") as in_file:
    wow_items = json.load(in_file)

replace = "'"


@lru_cache()
def item_look_up(message: str):
    items = re.findall(r"{[a-zA-Z0-9,\-.' ]+}", message)

    urls = []
    for item_name in items:
        item_name = item_name.replace("{", "").replace("}", "")

        try:
            item_id = wow_items[item_name]
        except KeyError:
            levs = {
                levenshtein_distance(item_name, key): key
                for key in wow_items.keys() if key[0].lower() == item_name[0].lower()
            }

            item_name = levs[min(levs.keys())]
            item_id = wow_items[item_name]

        urls.append(make_url(item_id, item_name))

    return "\n".join(urls)


def make_url(item_id: int, item_name: str):
    return f"https://tbc.wowhead.com/item={item_id}/{'-'.join(item_name.replace(replace, '').lower().split())}"
