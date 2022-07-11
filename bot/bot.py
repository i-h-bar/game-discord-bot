import asyncio
import io
import os
from base64 import b64decode

import discord
from discord import Message, DMChannel, RawReactionActionEvent
from discord.ext import commands
from tortoise import Tortoise

from dnd.api import get_spell
from dnd.formatting.message import format_spell
from edge.messages.help import EDGE_HELP
from mtg.scryfall import search_scryfall
from table_top.calculator import calculate_from_message
from table_top.coin import flip_coin
from table_top.roller import get_roll
from utils.dev.measurement import async_time_it
from utils.discord import determine_send_function
from utils.help import HELP_MESSAGE
from utils.role_assignment import assign_from_reaction
from wow.parse import item_look_up
from wow.wrath.polling_collector import collect_result


bot = commands.Bot(command_prefix="/")


@bot.event
async def on_ready():
    await Tortoise.init(
        db_url='sqlite://wow/data/items.sqlite3',
        modules={'models': ['wow.data.models']}
    )

    print("Game bot initialised")


@bot.event
@async_time_it
async def on_message(message: Message):
    if message.author == bot.user:
        return

    if not isinstance(message.channel, DMChannel) and "wrath-class-poll" in message.channel.name:
        await collect_result(message)

    send_message = determine_send_function(message)

    if message.content.startswith("/r") or message.content.startswith("/roll"):
        message.content = message.content.replace("/roll", "").replace("/r", "")
        await send_message(f"{message.author.mention} {get_roll(message)}")

    elif message.content.startswith("/c"):
        await send_message(calculate_from_message(message))

    elif message.content.startswith("/s"):
        spell_name = message.content.replace("/search", "").replace("/s", "").strip()

        for reply in await format_spell(message, spell_name, await get_spell(spell_name)):
            await send_message(reply)

    elif message.content.startswith("/flip"):
        await send_message(await flip_coin(message))

    elif "[[" in message.content and "]]" in message.content:
        async for card_info, card_image in await search_scryfall(message):
            reply = f"{message.author.mention}\n"
            await send_message(
                reply,
                file=discord.File(io.BytesIO(card_image), f"{card_info.get('name', 'default').replace(' ', '_')}.png")
            )
            await asyncio.sleep(0.05)

    elif "{{" in message.content and "}}" in message.content:
        async for tooltip, url, name in item_look_up(message.content):
            if tooltip is not None:
                await send_message(f"<{url}>", file=discord.File(io.BytesIO(tooltip), f"{name}.png"))
            else:
                await send_message(url)

    elif message.content.startswith("/h"):
        if "edge" in message.content:
            await send_message(f"{message.author.mention}\n{EDGE_HELP}")
        else:
            await send_message(f"{message.author.mention}\n{HELP_MESSAGE}")

    elif message.content.startswith("/who"):
        x = 0

    elif message.content.strip().lower() == "good bot":
        await send_message(f"{message.author.mention} Thanks!")


@bot.event
async def on_raw_reaction_add(reaction: RawReactionActionEvent):
    channel = bot.get_channel(reaction.channel_id)
    if "role-assignment" in channel.name:
        await assign_from_reaction(reaction)


def run():
    bot.run(os.getenv("game_bot_token"))


if __name__ == "__main__":
    run()