import difflib
import re

from utils.dev.measurement import async_time_it
from utils.levensteine import distance
from cache import AsyncTTL

from utils.aio.wrappers import asyncify
from wow.data.items import wow_items

REPLACE_CHAR = "'"


async def item_look_up(message: str):
    return "\n".join(
        [make_url(*(await wow_fuzzy_match(item_name))) for item_name in re.findall(r"{{[a-zA-Z0-9,\-.' ]+}}", message)]
    )


def make_url(item_id: int, item_name: str):
    return f"https://tbc.wowhead.com/item={item_id}/{'-'.join(item_name.replace(REPLACE_CHAR, '').lower().split())}"


@async_time_it
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
            if distance(item_name, key) < 10
        }

        try:
            item_name = diff_ratios[max(diff_ratios.keys())]
        except ValueError:
            item_name = "dirge"
            item_id = wow_items[item_name]
        else:
            item_id = wow_items[item_name]

    return item_id, item_name
