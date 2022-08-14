import re
from string import punctuation, whitespace
from typing import Optional, AsyncIterable

from cache import AsyncTTL
from tortoise.exceptions import DoesNotExist

from utils.string_matching import consecutive_sequence_score
from wow.data.items import wow_items, item_starting_letters, starting_letter_groups
from wow.data.models import Items


async def item_look_up(message: str) -> AsyncIterable[tuple[Optional[bytes], str, str]]:
    items = [await wow_fuzzy_match(item_name) for item_name in re.findall(r"{{}}|{{[a-zA-Z0-9,\-.' ]+}}", message)]

    for item_id, item_name in items:
        try:
            tooltip = (await Items.get(id=item_id)).tooltip
        except DoesNotExist:
            yield None, make_url(item_id, item_name), item_name
        else:
            yield tooltip, make_url(item_id, item_name), item_name


def make_url(item_id: int, item_name: str):
    return f"https://wowhead.com/wotlk/item={item_id}/{item_name.replace(' ', '-')}"


def normalise(item: str) -> str:
    return re.sub(f"[{punctuation + whitespace}]+", " ", item).strip().lower()


async def matching_start_items(item_name: str) -> list[str]:
    try:
        return (await starting_letter_groups())[item_name[:2]]
    except (KeyError, IndexError):
        return []


@AsyncTTL(time_to_live=86400)
async def wow_fuzzy_match(item_name: str):
    item_name = normalise(item_name)
    try:
        item_id = wow_items[item_name]
    except KeyError:
        max_item = ""
        max_item_match = 0

        for item in await matching_start_items(item_name):
            if (num := (consecutive_sequence_score(item_name, item))) > max_item_match:
                max_item = item
                max_item_match = num

        if max_item:
            item_name = max_item
        else:
            item_name = "dirge"

        item_id = wow_items[item_name]

    return item_id, item_name
