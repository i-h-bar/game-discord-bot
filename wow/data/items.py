from collections import defaultdict
from cache import AsyncLRU

from utils.database import db
from utils.strings import normalise


@AsyncLRU()
async def encoded_item_names() -> list[bytes]:
    return [normalise(item["name"]).encode() for item in await db.all_item_names()]


@AsyncLRU()
async def normalised_items() -> dict[str, int]:
    return {normalise(item["name"]).encode(): item["item_id"] for item in await db.all_items_ids_and_names()}


@AsyncLRU()
async def item_starting_letters() -> dict[bytes, str]:
    return {item: set(word[:2] for word in item.split()) for item in (await normalised_items()).keys()}


@AsyncLRU()
async def item_starting_letter_groups() -> dict[str, list[bytes]]:
    starting_letter_groups = defaultdict(list)

    for item, starting_letters in (await item_starting_letters()).items():
        for starting_letter in starting_letters:
            starting_letter_groups[starting_letter].append(item)

    return starting_letter_groups
