import asyncio
import re
from operator import itemgetter
from string import punctuation, whitespace
from typing import Optional, AsyncIterable

from utils.string_matching import distance
from cache import AsyncTTL
from tortoise.exceptions import DoesNotExist

from utils.strings import async_sequence_score
from wow.data.items import wow_items, starting_letter_groups
from wow.data.models import Items


@AsyncTTL(time_to_live=86400)
async def get_item_tooltip(item_id: int) -> bytes:
    return (await Items.get(id=item_id)).tooltip


async def item_look_up(message: str) -> AsyncIterable[tuple[Optional[bytes], str, str]]:
    items = [await wow_fuzzy_match(item_name) for item_name in re.findall(r"{{}}|{{[a-zA-Z0-9,\-.' ]+}}", message)]

    for item_id, item_name in items:
        try:
            tooltip = await get_item_tooltip(item_id)
        except DoesNotExist:
            yield None, make_url(item_id, item_name), item_name
        else:
            yield tooltip, make_url(item_id, item_name), item_name


def make_url(item_id: int, item_name: str):
    return f"https://wowhead.com/wotlk/item={item_id}/{item_name.replace(' ', '-')}"


def normalise(item: str) -> str:
    return re.sub(f"[{punctuation + whitespace}]+", " ", item).strip().lower()


def matching_start_items(item_name: str) -> list[str]:
    try:
        return starting_letter_groups[item_name[:3]]
    except (KeyError, IndexError):
        return []


# @AsyncTTL(time_to_live=86400)
async def wow_fuzzy_match(item_name: str):
    item_name = normalise(item_name)
    try:
        item_id = wow_items[item_name]
    except KeyError:
        scores = await asyncio.gather(
            *(
                async_sequence_score(item_name, item)
                for item in matching_start_items(item_name) if distance(item_name, item) < 7
            )
        )

        if scores:
            item_name = max(scores, key=itemgetter(1))[0]
        else:
            item_name = "dirge"

        item_id = wow_items[item_name]

    return item_id, item_name
