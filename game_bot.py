import asyncio
import io
import os

import discord
from discord import Message
from discord.ext import commands

from dnd.api import get_spell
from dnd.formatting.message import format_spell
from edge.messages.help import EDGE_HELP
from mtg.scryfall import search_scryfall
from table_top.calculator import calculate_from_message
from table_top.coin import flip_coin
from table_top.dice.roller import get_roll
from utils.discord import determine_send_function
from utils.help import HELP_MESSAGE
from wow.parse import item_look_up

bot = commands.Bot(command_prefix="/")


@bot.event
async def on_ready():
    print("Game bot initialised")


@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return

    send_message = determine_send_function(message)

    if message.content.startswith("/r") or message.content.startswith("/roll"):
        message.content = message.content.replace("/roll", "").replace("/r", "")
        await send_message(get_roll(message))

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

    elif "{" in message.content and "}" in message.content:
        await send_message(await item_look_up(message.content))

    elif message.content.startswith("/h"):
        if "edge" in message.content:
            await send_message(f"{message.author.mention}\n{EDGE_HELP}")
        else:
            await send_message(f"{message.author.mention}\n{HELP_MESSAGE}")


bot.run(os.getenv("game_bot_token"))
