import re
from string import punctuation, whitespace
from typing import Optional

from cache import AsyncTTL
from tortoise.exceptions import DoesNotExist

from utils.string_matching import consecutive_sequence_score
from wow.data.items import wow_items, item_starting_letters
from wow.data.models import Items


async def item_look_up(message: str) -> tuple[Optional[bytes], str, str]:
    items = [await wow_fuzzy_match(item_name) for item_name in re.findall(r"{{}}|{{[a-zA-Z0-9,\-.' ]+}}", message)]

    for item_id, item_name in items:
        try:
            tooltip = (await Items.get(id=item_id)).tooltip
        except DoesNotExist:
            yield None, make_url(item_id, item_name), item_name
        else:
            yield tooltip, make_url(item_id, item_name), item_name


def make_url(item_id: int, item_name: str):
    return f"https://tbc.wowhead.com/item={item_id}/{item_name.replace(' ', '-')}"


def normalise(item: str) -> str:
    return re.sub(f"[{punctuation + whitespace}]+", " ", item).strip().lower()


@AsyncTTL(time_to_live=86400)
async def wow_fuzzy_match(item_name: str):
    item_name = normalise(item_name)
    try:
        item_id = wow_items[item_name]
    except KeyError:
        items = (item for item in wow_items.keys() if item_name[:2] in item_starting_letters[item])

        max_item = ""
        max_item_match = 0

        for item in items:
            if (num := (consecutive_sequence_score(item_name, item))) > max_item_match:
                max_item = item
                max_item_match = num

        if max_item:
            item_name = max_item
        else:
            item_name = "dirge"

        item_id = wow_items[item_name]

    return item_id, item_name