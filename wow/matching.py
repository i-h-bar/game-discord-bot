import asyncio
from operator import itemgetter

from cache import AsyncTTL

from utils.dev.measurement import async_time_it
from utils.string_matching import levenshtein_distance, index_below_threshold
from utils.strings import async_sequence_score, normalise
from wow.data.items import encoded_item_names


def make_url(item_id: int, item_name: str, area: str):
    return f"https://wowhead.com/wotlk/{area}={item_id}/{normalise(item_name).replace(' ', '-')}"


async def matching_start_items(item_name: str, starting_letters: callable) -> list[bytes]:
    try:
        return (await starting_letters())[item_name[:3]]
    except (KeyError, IndexError):
        return []


# @async_time_it
# @AsyncTTL(time_to_live=86400)
async def wow_fuzzy_match(name: str, starting_letters: callable, normalised_names: callable):
    name = normalise(name)
    items = await matching_start_items(name, starting_letters)
    score = 100_000_000
    try:
        item_id = (await normalised_names())[name]
    except KeyError:
        scores = await asyncio.gather(
            *(
                async_sequence_score(name, items[i].decode()) for i in index_below_threshold(name.encode(), items)
            )
        )

        if scores:
            name, score = max(scores, key=itemgetter(1))
        else:
            name, score = "dirge", 0

        item_id = (await normalised_names())[name]

    return item_id, name, score
