import asyncio

from typing import Tuple
from requests_handler import async_get


SCRYFALL = "https://api.scryfall.com"
CARD_SEARCH_API = "/cards/named"
FUZZY = "?fuzzy="


async def get_card(card_name: str) -> Tuple[dict, bytes]:
    card_name_param = "+".join(card_name.split())
    card_info = await async_get(f"{SCRYFALL}{CARD_SEARCH_API}{FUZZY}{card_name_param}")
    await asyncio.sleep(0.05)
    card_image = await async_get(card_info["image_uris"]["normal"], False)

    return card_info, card_image.content
