import asyncio

from requests_handler.async_requests import async_get
from utility_functions.levenshtein import levenshtein_distance

DND_API = "https://www.dnd5eapi.co"

SPELL = "/api/spells/"


async def get_spell(spell_name):
    spell_info = await async_get(f"{DND_API}{SPELL}?name={'+'.join(spell_name.split())}")

    if spell_info["count"] > 0:
        levenshteins = {
            await levenshtein_distance(spell_name, spell["name"]): spell["url"] for spell in spell_info["results"]
        }
    else:
        await asyncio.sleep(0.05)
        spell_info = await async_get(f"{DND_API}{SPELL}")
        levenshteins = {
            await levenshtein_distance(spell_name, spell["name"]): spell["url"] for spell in spell_info["results"]
        }

    await asyncio.sleep(0.05)

    return await async_get(f"{DND_API}{levenshteins[min(levenshteins.keys())]}")
