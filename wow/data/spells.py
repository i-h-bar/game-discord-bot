from collections import defaultdict

from cache import AsyncLRU

from utils.database import db
from utils.strings import normalise


@AsyncLRU()
async def normalised_spells() -> dict[bytes, tuple[int, str]]:
    return {
        normalise(spell["name"]).encode(): (spell["spell_id"], "spell") for spell in await db.all_spells_ids_and_names()
    }


@AsyncLRU()
async def spell_starting_letters() -> dict[bytes, str]:
    return {spell: set(word[:3] for word in spell.split()) for spell in (await normalised_spells()).keys()}


@AsyncLRU()
async def spell_starting_letter_groups() -> dict[bytes, list[bytes]]:
    starting_letter_groups = defaultdict(list)

    for spell, starting_letters in (await spell_starting_letters()).items():
        for starting_letter in starting_letters:
            starting_letter_groups[starting_letter].append(spell)

    return starting_letter_groups
