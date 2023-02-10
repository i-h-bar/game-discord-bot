from utils.string_matching import get_closest_match
from utils.strings import normalise


def make_url(item_id: int, item_name: str, area: str):
    return f"https://wowhead.com/wotlk/{area}={item_id}/{normalise(item_name).replace(' ', '-')}"


async def wow_fuzzy_match(
        name: str, starting_letters: dict[bytes, list[bytes]], normalised_names: dict[bytes, tuple[int, str]]
):
    name = normalise(name).encode()
    try:
        item_id, table = normalised_names[name]
    except KeyError:
        name = get_closest_match(name, starting_letters)
        item_id, table = normalised_names[name]

    return item_id, name.decode(), table
