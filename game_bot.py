import asyncio
import io
import os

import discord

from discord.ext import commands

from constants.help import HELP_MESSAGE
from dnd_functions.dnd_api import get_spell
from dnd_functions.message_formatting.message_formatting import format_spell
from edge_functions.pre_built_messages.help_messages import edge_help
from mtg_functions.scryfall import search_scryfall
from table_top_items.calculator import calculate_from_message
from table_top_items.coin import flip_coin
from table_top_items.dice_parser import get_roll


bot = commands.Bot(command_prefix="/")


@bot.event
async def on_ready():
    print("Game bot initialised")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    channel = message.channel

    if message.content.startswith("/r") or message.content.startswith("/roll"):
        message.content = message.content.replace("/roll", "").replace("/r", "")
        await channel.send(await get_roll(message))

    elif message.content.startswith("/c"):
        await channel.send(await calculate_from_message(message))

    elif message.content.startswith("/s"):
        spell_name = message.content.replace("/search", "").replace("/s", "").strip()

        for reply in await format_spell(message, spell_name, await get_spell(spell_name)):
            await channel.send(reply)

    elif message.content.startswith("/flip"):
        await channel.send(await flip_coin(message))

    elif "[[" in message.content and "]]" in message.content:
        async for card_info, card_image in await search_scryfall(message):
            reply = f"{message.author.mention}\n"
            await channel.send(
                reply,
                file=discord.File(io.BytesIO(card_image), f"{card_info.get('name', 'default').replace(' ', '_')}.png")
            )
            await asyncio.sleep(0.05)

    elif message.content.startswith("/h"):
        if "edge" in message.content:
            await channel.send(f"{message.author.mention}\n{edge_help}")
        else:
            await channel.send(f"{message.author.mention}\n{HELP_MESSAGE}")


bot.run(os.getenv("game_bot_token"))
