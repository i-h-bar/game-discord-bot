import os
from discord.ext import commands

from mtg_discord_bot import mtg_bot
from dnd_discord_bot import dnd_bot
from edge_discord_bot import edge_bot

from constants.help import HELP_MESSAGE
from game_bot_functions.game_tracking import tracker
from game_bot_functions.games import MTG, DND, EDGE

bot = commands.Bot(command_prefix=("/", "!"))


@bot.event
async def on_ready():
    print("Game bot initialised")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!set"):
        content = message.content

        if content.replace("!set", "").lower().strip() == MTG:
            tracker[message.channel.id] = MTG
            await message.channel.send(f"{message.author.mention} Game set to - Magic the Gathering")

        elif content.replace("!set", "").lower().strip() == DND:
            tracker[message.channel.id] = DND
            await message.channel.send(f"{message.author.mention} Game set to - Dungeons & Dragons")

        elif content.replace("!set", "").lower().strip() == EDGE:
            tracker[message.channel.id] = EDGE
            await message.channel.send(f"{message.author.mention} Game set to - Star Wars: Edge of the Empire")

    elif message.content.startswith("!game"):
        if tracker.get(message.channel.id) == MTG:
            current_game = "Magic the Gathering"
        elif tracker.get(message.channel.id) == DND:
            current_game = "Dungeons & Dragons"
        elif tracker.get(message.channel.id) == EDGE:
            current_game = "Star Wars: Edge of the Empire"
        else:
            current_game = "none"

        await message.channel.send(f"{message.author.mention} Game is currently - {current_game}.")

    elif message.content.startswith("!help") or \
            (message.content.startswith("/help") and tracker.get(message.channel.id) is None):
        await message.channel.send(f"{message.author.mention} \n" + HELP_MESSAGE)

    elif tracker.get(message.channel.id) == MTG:
        await mtg_bot.on_message(message)

    elif tracker.get(message.channel.id) == DND:
        await dnd_bot.on_message(message)

    elif tracker.get(message.channel.id) == EDGE:
        await edge_bot.on_message(message)

    elif message.content.startswith("/r") or message.content.startswith("/roll"):
        await dnd_bot.on_message(message)

    elif message.content.startswith("/c"):
        await dnd_bot.on_message(message)

    elif message.content.startswith("/s dnd"):
        message.content = message.content.replace("dnd", "")
        await dnd_bot.on_message(message)

    elif message.content.startswith("/s mtg"):
        message.content = message.content.replace("dnd", "")
        await mtg_bot.on_message(message)


bot.run(os.getenv("game_bot_token"))
