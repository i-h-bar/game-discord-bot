import asyncio
import difflib

from Levenshtein import distance

from dnd.constants import DND_API, SPELL
from utils.aio.requests import async_get


async def get_spell(spell_name):
    spell_info = await async_get(f"{DND_API}{SPELL}?name={'+'.join(spell_name.split())}")

    if spell_info["count"] == 1:
        difference_scores = {
            3000: spell_info["results"][-1]["url"]
        }

    elif spell_info["count"] > 0:
        difference_scores = {
            difflib.SequenceMatcher(a=spell_name, b=spell["name"]).ratio(): spell["url"]
            for spell in spell_info["results"] if distance(spell_name, spell["name"]) < 10
        }
    else:
        await asyncio.sleep(0.05)
        spell_info = await async_get(f"{DND_API}{SPELL}")
        difference_scores = {
            difflib.SequenceMatcher(a=spell_name, b=spell["name"]).ratio(): spell["url"]
            for spell in spell_info["results"] if distance(spell_name, spell["name"]) > 0.5
        }

    await asyncio.sleep(0.05)

    return await async_get(f"{DND_API}{difference_scores[max(difference_scores.keys())]}")
