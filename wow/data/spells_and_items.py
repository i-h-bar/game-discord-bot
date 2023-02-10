from collections import defaultdict

from cache import AsyncLRU

from utils.database import db
from utils.strings import normalise


@AsyncLRU()
async def normalised_objects() -> dict[bytes, tuple[int, str]]:
    return {
        name: info for name, info in
        [
            (normalise(spell["name"]).encode(), (spell["spell_id"], "spell")) for spell in
            await db.all_spells_ids_and_names()
        ] +
        [
            (normalise(item["name"]).encode(), (item["item_id"], "item")) for item in await db.all_items_ids_and_names()
        ]
    }


@AsyncLRU()
async def object_starting_letters() -> dict[bytes, str]:
    return {spell: set(word[:3] for word in spell.split()) for spell in (await normalised_objects()).keys()}


@AsyncLRU()
async def object_starting_letter_groups() -> dict[bytes, list[bytes]]:
    starting_letter_groups = defaultdict(list)

    for spell, starting_letters in (await object_starting_letters()).items():
        for starting_letter in starting_letters:
            starting_letter_groups[starting_letter].append(spell)

    return starting_letter_groups
