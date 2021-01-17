import os
import io
import discord
import asyncio

from mtg_functions.scryfall import get_card
from table_top_items.coin import flip_coin

from table_top_items.calculator import calculate

from table_top_items.dice import roll_dice
from discord.ext import commands


async def on_ready():
    print("Bot initialised")


async def on_message(message):
    if message.content.startswith("/r") or message.content.startswith("/roll"):
        await roll_dice(message)

    elif message.content.startswith("/c"):
        channel = message.channel
        reply = f"{message.author.mention} `{message.content.replace(' ', '').replace('/c', '').strip()}` = "
        reply += str(await calculate(message.content.replace("/c", "")))
        await channel.send(reply)

    elif message.content.startswith("/flip"):
        await flip_coin(message)

    elif message.content.startswith("/s") or message.content.startswith("/search"):
        channel = message.channel
        card_names = message.content.replace("/search", "").replace("/s", "").strip()
        reply = f"{message.author.mention}\n"

        for card_name in card_names.split("+"):
            card_info, card_image = await get_card(card_name)
            await channel.send(
                reply,
                file=discord.File(io.BytesIO(card_image),
                                  f"{card_info.get('name', 'default').replace(' ', '_')}.png")
            )
            await asyncio.sleep(0.05)

    elif message.content.startswith("/help") or message.content.startswith("/h"):
        channel = message.channel
        reply = f"{message.author.mention}\n"

        await channel.send(reply)


if __name__ == "__main__":
    bot = commands.Bot(command_prefix="/")

    on_read = bot.event(on_ready)
    on_message = bot.event(on_message)

    bot.run(os.getenv("mtg_bot_token"))
