import asyncio
import re
from operator import itemgetter
from string import punctuation
from typing import Optional, AsyncIterable

from cache import AsyncTTL

from utils.database import db
from utils.string_matching import distance
from utils.strings import async_sequence_score, normalise
from wow.data.items import normalised_items, item_starting_letter_groups
from wow.data.spells import spell_starting_letter_groups, normalised_spells


@AsyncTTL(time_to_live=86400)
async def get_item_tooltip(item_id: int) -> bytes:
    return await db.tooltip_from_item_id(item_id)


@AsyncTTL(time_to_live=86400)
async def get_spell_tooltip(spell_id: int) -> bytes:
    return await db.tooltip_from_spell_id(spell_id)


async def wow_look_up(message: str) -> AsyncIterable[tuple[Optional[bytes], str, str]]:
    items = [
        await wow_fuzzy_match(item_name, item_starting_letter_groups, normalised_items)
        for item_name in re.findall(r"{{}}|{{[a-zA-Z0-9,\-.' ]+}}", message)
    ]

    spells = [
        await wow_fuzzy_match(item_name, spell_starting_letter_groups, normalised_spells)
        for item_name in re.findall(r"{{}}|{{[a-zA-Z0-9,\-.' ]+}}", message)
    ]

    for (item_id, item_name, item_score), (spell_id, spell_name, spell_score) in zip(items, spells):
        if item_score > spell_score:
            yield await get_item_tooltip(item_id), make_url(item_id, item_name, "item"), item_name
        else:
            yield await get_spell_tooltip(spell_id), make_url(spell_id, spell_name, "spell"), spell_name


def make_url(item_id: int, item_name: str, area: str):
    return f"https://wowhead.com/wotlk/{area}={item_id}/{normalise(item_name).replace(' ', '-')}"


async def matching_start_items(item_name: str, starting_letters: callable) -> list[str]:
    try:
        return (await starting_letters())[item_name[:3]]
    except (KeyError, IndexError):
        return []


# @AsyncTTL(time_to_live=86400)
async def wow_fuzzy_match(name: str, starting_letters: callable, normalised_names: callable):
    name = normalise(name)
    score = 100_000_000
    try:
        item_id = (await normalised_names())[name]
    except KeyError:
        scores = await asyncio.gather(
            *(
                async_sequence_score(name, item)
                for item in await matching_start_items(name, starting_letters) if distance(name, item) < 7
            )
        )

        if scores:
            name, score = max(scores, key=itemgetter(1))
        else:
            name, score = "dirge", 0

        item_id = (await normalised_names())[name]

    return item_id, name, score
