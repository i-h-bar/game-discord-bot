import re
from collections import defaultdict

import discord
from discord import Message
from tortoise.exceptions import DoesNotExist

from wow.data.models import Items
from wow.parse import wow_fuzzy_match


async def get_profession(item_id: int) -> tuple[str, bytes] | tuple[None, None]:
    try:
        items = await Items.filter(id=item_id)
    except DoesNotExist:
        return None, None
    else:
        profession_filter = tuple(item for item in items if item.profession is not None)

        if len(profession_filter) == 1:
            return profession_filter[0].profession, profession_filter[0].tooltip
        else:
            return None, items[0].tooltip


async def profession_map(message: Message) -> tuple[dict | None, list[tuple[bytes, str]] | None]:
    items = [
        await wow_fuzzy_match(item_name) for item_name in re.findall(r"{{}}|{{[a-zA-Z0-9,\-.' ]+}}", message.content)
    ]
    professions = defaultdict(list)
    tooltips = []
    for item_id, item_name in items:
        profession, tooltip = await get_profession(item_id)

        if profession is None and tooltip is None:
            return None, None

        if profession is None:
            professions["not prof crafted"].append(item_name)
        else:
            professions[profession].append(item_name)
            tooltips.append((tooltip, item_name))

    return professions, tooltips


async def professions_reply(message: Message) -> tuple[str | None, list[tuple[bytes, str]] | None]:
    reply = ""
    professions, tooltips = await profession_map(message)

    if professions is None and tooltips is None:
        return None, None

    for profession, wanted_items in professions.items():
        role = discord.utils.get(message.guild.roles, name=profession)
        if role is not None:
            reply += (
                f"Hey there {role.mention} can you make "
                f"[{', '.join(f'**{item.title()}**' for item in wanted_items)}] for {message.author.mention}\n"
            )

    if "not prof crafted" in professions:
        reply += (
            f"Sorry [{', '.join(f'**{item.title()}**' for item in professions['not prof crafted'])}]"
            f" can't be crafted by a profession :("
        )

    return reply, tooltips
