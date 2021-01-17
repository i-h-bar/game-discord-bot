import re
import os
import edge_functions.pre_built_messages.help_messages as hm

from discord.ext import commands
from edge_functions.dice_logic.dice_roller import roll
from edge_functions.dice_logic.command_map import dice_map


async def on_ready():
    print("Bot initialised")


async def on_message(message):
    if message.content.startswith("/r"):
        channel = message.channel
        reply = f"{message.author.mention}"
        for dice_roll in message.content.replace("/r", "").split("+"):
            try:
                times = int(re.findall(r'\d+', dice_roll)[0])
            except IndexError:
                times = 1

            die = re.sub(r"[0-9]", "", dice_roll).strip().lower()

            if die not in list(dice_map.keys()):
                reply += "\nMeow"
            else:
                for key, value in dice_map.items():
                    if key == die:
                        reply += f"\n`{value['dice name']}` = {roll(value['dice faces'], times)}"
                        break

        await channel.send(reply)

    elif message.content.startswith("/help") or message.content.startswith("/h"):
        channel = message.channel
        reply = f"{message.author.mention}\n"
        if "dice" in message.content or "symbols" in message.content:
            reply += hm.dice_help
        elif "roll" in message.content or "rolling" in message.content:
            reply += hm.rolling_help
        else:
            reply += f"{hm.rolling_help}\n\nResult symbols:\n{hm.dice_help}"

        await channel.send(reply)


if __name__ == "__main__":
    bot = commands.Bot(command_prefix="/")

    on_read = bot.event(on_ready)
    on_message = bot.event(on_message)

    bot.run(os.getenv("edge_bot_token"))
