import asyncio
import re
from typing import Tuple

from utils.aio.requests import async_get

SCRYFALL = "https://api.scryfall.com"
CARD_SEARCH_API = "/cards/named"
FUZZY = "?fuzzy="


async def search_scryfall(message):
    card_names = re.findall(r"\[\[[a-zA-Z0-9,\-.' ]+]]", message.content)
    return (await get_card(card_name) for card_name in card_names)


async def get_card(card_name: str) -> Tuple[dict, bytes]:
    card_name_param = "+".join(card_name.replace("[", "").replace("]", "").split())
    card_info = await async_get(f"{SCRYFALL}{CARD_SEARCH_API}{FUZZY}{card_name_param}")
    await asyncio.sleep(0.05)
    card_image = await async_get(card_info["image_uris"]["normal"], False)

    return card_info, card_image.content
