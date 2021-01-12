import os
from discord.ext import commands

from mtg_discord_bot import mtg_bot

from game_bot_functions.game_tracking import tracker
from game_bot_functions.games import MTG

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

        if content.replace("!set", "").lower().strip() == "mtg":
            set_game = MTG
            tracker[message.channel.id] = set_game
            await message.channel.send(f"{message.author.mention} Game set to - {MTG}")

    elif message.content.startswith("!game"):
        if tracker.get(message.channel.id) == MTG:
            current_game = "Magic the Gathering"
        else:
            current_game = "none"

        await message.channel.send(f"{message.author.mention} Game is currently - {current_game}.")

    elif tracker.get(message.channel.id) == MTG:
        await mtg_bot.on_message(message)

    elif tracker.get(message.channel.id) is None:
        await message.channel.send(f"{message.author.mention} - You have not set your game")

    print(tracker)


bot.run(os.getenv("game_bot_token"))
