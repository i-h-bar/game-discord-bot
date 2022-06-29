import re
from string import punctuation, whitespace

from cache import AsyncTTL

from utils.dev.measurement import async_time_it
from utils.string_matching import longest_sequence
from wow.data.items import wow_items


async def item_look_up(message: str):
    return "\n".join(
        [make_url(*(await wow_fuzzy_match(item_name))) for item_name in re.findall(r"{{}}|{{[a-zA-Z0-9,\-.' ]+}}", message)]
    )


def make_url(item_id: int, item_name: str):
    return f"https://tbc.wowhead.com/item={item_id}/{item_name.replace(' ', '-')}"


def normalise(item: str) -> str:
    return re.sub(f"[{punctuation + whitespace}]+", " ", item).strip().lower()


@async_time_it
@AsyncTTL(time_to_live=86400)
async def wow_fuzzy_match(item_name: str):
    item_name = normalise(item_name)
    try:
        item_id = wow_items[item_name]
    except KeyError:
        items = (item for item in wow_items.keys() if item[0: 2] == item_name[0: 2])

        max_item = ""
        max_item_match = 0

        for item in items:
            if (num := longest_sequence(item_name, item)) > max_item_match:
                max_item = item
                max_item_match = num

        if max_item:
            item_name = max_item
        else:
            item_name = "dirge"

        item_id = wow_items[item_name]

    return item_id, item_name
