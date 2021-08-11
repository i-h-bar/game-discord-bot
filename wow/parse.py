import difflib
import json
import re

from cache import AsyncTTL

from utils.aio.wrappers import asyncify
from utils.strings import quick_gestalt

with open("wow/data/items.json", "r") as in_file:
    wow_items = json.load(in_file)

REPLACE_CHAR = "'"


async def item_look_up(message: str):
    return "\n".join(
        [make_url(*(await wow_fuzzy_match(item_name))) for item_name in re.findall(r"{[a-zA-Z0-9,\-.' ]+}", message)]
    )


def make_url(item_id: int, item_name: str):
    return f"https://tbc.wowhead.com/item={item_id}/{'-'.join(item_name.replace(REPLACE_CHAR, '').lower().split())}"


@AsyncTTL(time_to_live=86400)
@asyncify
def wow_fuzzy_match(item_name: str):
    item_name = item_name.replace("{", "").replace("}", "")
    try:
        item_id = wow_items[item_name]
    except KeyError:
        diff_ratios = {
            difflib.SequenceMatcher(a=item_name, b=key).ratio(): key
            for key in wow_items.keys()
            if quick_gestalt(item_name, key) > 0.75
        }

        try:
            item_name = diff_ratios[max(diff_ratios.keys())]
        except ValueError:
            item_name = "dirge"
            item_id = wow_items[item_name]
        else:
            item_id = wow_items[item_name]

    return item_id, item_name
