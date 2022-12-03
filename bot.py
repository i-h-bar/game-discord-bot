import io
import os

import discord
from discord import Message, app_commands
from discord.ext import commands

from table_top.calculator import calculate_from_message
from table_top.coin import flip_coin
from table_top.roller import get_roll
from utils.database import db
from wow.data.items import item_starting_letter_groups
from wow.data.spells import spell_starting_letter_groups
from wow.items import item_look_up
from wow.spells import spell_look_up


class Bot(commands.Bot):
    async def close(self):
        await db.close()
        await super().close()
        print("Bot Closed Down")


bot = Bot(command_prefix="/", intents=discord.Intents.all())


@bot.event
async def on_ready():
    await db.connect()
    await item_starting_letter_groups()
    await spell_starting_letter_groups()

    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")
    print("Game bot initialised")


@bot.tree.command(name="echo")
@app_commands.describe(message="message")
async def echo(interaction: discord.Integration, message: str):
    await interaction.response.send_message(message)


@bot.tree.command(name="num_of_guilds")
async def num_of_guilds(interaction: discord.Integration):
    if interaction.user.id == "":
        await interaction.response.send_message(len(bot.guilds), ephemeral=True)


@bot.tree.command(name="item")
@app_commands.describe(item_name="Item to get (Fuzzy matches so don't worry if you mistype)")
@app_commands.describe(hide="Show everyone the bot response yes / no")
async def get_item(interaction: discord.Integration, item_name: str, hide: str = None):
    tooltip, url, name = await item_look_up(item_name)

    await interaction.response.send_message(
        f"<{url}>",
        file=discord.File(io.BytesIO(tooltip), f"{name}.png"),
        ephemeral=True if hide == "yes" else False
    )


@bot.tree.command(name="spell")
@app_commands.describe(spell_name="Spell to get (Fuzzy matches so don't worry if you mistype)")
@app_commands.describe(hide="Show everyone the bot response yes / no")
async def get_item(interaction: discord.Integration, spell_name: str, hide: str = None):
    tooltip, url, name = await spell_look_up(spell_name)

    await interaction.response.send_message(
        f"<{url}>",
        file=discord.File(io.BytesIO(tooltip), f"{name}.png"),
        ephemeral=True if hide == "yes" else False
    )


@bot.tree.command(name="roll")
@app_commands.describe(dice="Size and number of dice to roll")
@app_commands.describe(hide="Hide the dice roll yes / no")
async def roll_dice(interaction: discord.Integration, dice: str, hide: str = None):
    await interaction.response.send_message(
        f"{interaction.user.mention} {get_roll(dice)}",
        ephemeral=True if hide == "yes" else False
    )


@bot.tree.command(name="calc")
@app_commands.describe(expression="Expression to calculate")
async def calculate(interaction: discord.Integration, expression: str):
    return await interaction.response.send_message(calculate_from_message(expression))


@bot.tree.command(name="flip")
@app_commands.describe(number_of_flips="Number of times to flip the coin")
async def flip(interaction: discord.Integration, number_of_flips: str):
    return await interaction.response.send_message(await flip_coin(number_of_flips))


@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return

    # elif "[[" in message.content and "]]" in message.content:
    #     async for card_info, card_image in await search_scryfall(message):
    #         reply = f"{message.author.mention}\n"
    #         await send_message(
    #             reply,
    #             file=discord.File(io.BytesIO(card_image), f"{card_info.get('name', 'default').replace(' ', '_')}.png")
    #         )
    #         await asyncio.sleep(0.05)
    #
    # elif message.content.startswith("/h"):
    #     if "edge" in message.content:
    #         await send_message(f"{message.author.mention}\n{EDGE_HELP}")
    #     else:
    #         await send_message(f"{message.author.mention}\n{HELP_MESSAGE}")
    #
    # elif message.content.strip().lower() == "good bot":
    #     await send_message(f"{message.author.mention} Thanks!")


def run():
    bot.run(os.getenv("game_bot_token"))


if __name__ == "__main__":
    run()
