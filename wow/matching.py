import asyncio
from operator import itemgetter

from cache import AsyncTTL

from utils.string_matching import distance
from utils.strings import async_sequence_score, normalise


def make_url(item_id: int, item_name: str, area: str):
    return f"https://wowhead.com/wotlk/{area}={item_id}/{normalise(item_name).replace(' ', '-')}"


async def matching_start_items(item_name: str, starting_letters: callable) -> list[str]:
    try:
        return (await starting_letters())[item_name[:3]]
    except (KeyError, IndexError):
        return []


@AsyncTTL(time_to_live=86400)
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
