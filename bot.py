import io
import os

import discord
from discord import app_commands
from discord.ext import commands

from edge.help_message import EDGE_HELP
from mtg.help_message import MTG_HELP
from mtg.scryfall import search_scryfall
from table_top.calculator import calculate_from_message
from table_top.coin.flip import flip_coin_until, flip_coin
from table_top.help_message import GENERAL_HELP
from table_top.roller import get_roll
from utils.database import db
from wow.data.items import item_starting_letter_groups
from wow.data.spells import spell_starting_letter_groups
from wow.help_message import WOW_HELP
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
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Slash Commands"))
    print("id: ", bot.application_id)
    synced = await bot.tree.sync()

    print(f"Synced {len(synced)} commands")
    print("Game bot initialised")


@bot.tree.command(name="help", description="Get help with using the bot for a particular game.")
@app_commands.describe(game="Which game's commands you wish to get help with")
@app_commands.choices(game=[
    app_commands.Choice(name="World of Warcraft", value="wow"),
    app_commands.Choice(name="Magic the Gathering", value="mtg"),
    app_commands.Choice(name="Star Wars: Edge of the Empire", value="sweote"),
    app_commands.Choice(name="General", value="general")
])
async def help_command(interaction: discord.Integration, game: str):
    if game == "wow":
        help_msg = WOW_HELP
    elif game == "mtg":
        help_msg = MTG_HELP
    elif game == "sweote":
        help_msg = EDGE_HELP
    else:
        help_msg = GENERAL_HELP

    return await interaction.response.send_message(help_msg, ephemeral=True)


@bot.tree.command(name="item", description="Search for an item in Wrath of the Lich King Classic (Fuzzy Matches)")
@app_commands.describe(item_name="Item to get (Fuzzy matches so don't worry if you mistype)")
@app_commands.describe(hide="Hide the item response Yes/No")
@app_commands.choices(hide=[
    app_commands.Choice(name="Yes", value=True),
    app_commands.Choice(name="No", value=False),
])
async def get_item(interaction: discord.Integration, item_name: str, hide: int = None):
    tooltip, url, name = await item_look_up(item_name)

    await interaction.response.send_message(
        f"<{url}>",
        file=discord.File(io.BytesIO(tooltip), f"{name}.png"),
        ephemeral=bool(hide)
    )


@bot.tree.command(name="spell", description="Search for an spell in Wrath of the Lich King Classic (Fuzzy Matches)")
@app_commands.describe(spell_name="Spell to get (Fuzzy matches so don't worry if you mistype)")
@app_commands.describe(hide="Hide the spell response Yes/No")
@app_commands.choices(hide=[
    app_commands.Choice(name="Yes", value=True),
    app_commands.Choice(name="No", value=False),
])
async def get_spell(interaction: discord.Integration, spell_name: str, hide: int = None):
    tooltip, url, name = await spell_look_up(spell_name)

    await interaction.response.send_message(
        f"<{url}>",
        file=discord.File(io.BytesIO(tooltip), f"{name}.png"),
        ephemeral=bool(hide)
    )


@bot.tree.command(name="roll", description="Roll any number/size of numerical or SW:EotE dice.")
@app_commands.describe(dice="Size and number of dice to roll")
@app_commands.describe(hide="Hide the dice roll Yes/No")
@app_commands.choices(hide=[
    app_commands.Choice(name="Yes", value=True),
    app_commands.Choice(name="No", value=False),
])
async def roll_dice(interaction: discord.Integration, dice: str, hide: int = None):
    await interaction.response.send_message(get_roll(dice), ephemeral=bool(hide))


@bot.tree.command(name="calc", description="Run a simple numerical calculation")
@app_commands.describe(expression="Expression to calculate")
async def calculate(interaction: discord.Integration, expression: str):
    return await interaction.response.send_message(calculate_from_message(expression))


@bot.tree.command(name="flip", description="Flip a coin x amount of times")
@app_commands.describe(number_of_flips="Number of times to flip the coin")
async def flip(interaction: discord.Integration, number_of_flips: str):
    return await interaction.response.send_message(await flip_coin(number_of_flips))


@bot.tree.command(name="flip_until", description="Keep flipping coins until a result is flipped")
@app_commands.describe(face="The loss condition")
@app_commands.describe(with_thumb="Use the Karak's Thumb rules in determining the coin flips")
@app_commands.choices(face=[
    app_commands.Choice(name="Heads", value="Heads"),
    app_commands.Choice(name="Tails", value="Tails"),
])
@app_commands.choices(with_thumb=[
    app_commands.Choice(name="Yes", value=True),
    app_commands.Choice(name="No", value=False),
])
async def flip_until(interaction: discord.Integration, face: str, with_thumb: int = None):
    return await interaction.response.send_message(flip_coin_until(face, with_thumb))


@bot.tree.command(
    name="search",
    description="Search from an Item or Spell in Wrath of the Lich King Classic (Fuzzy Matches)"
)
@app_commands.describe(name="Item or Spell to search (Fuzzy matches)")
async def get_spell_or_item(interaction: discord.Integration, name: str):
    return interaction.response.send_message(name)


@bot.tree.command(name="card", description="Search for a Magic the Gathering card (Fuzzy Matches)")
@app_commands.describe(name="Card name to search")
async def get_card(interaction: discord.Integration, name: str):
    card_info, card_image = await search_scryfall(name)
    return await interaction.response.send_message(
        file=discord.File(io.BytesIO(card_image), f"{card_info.get('name', 'default').replace(' ', '_')}.png")
    )


def run():
    bot.run(os.getenv("game_bot_token"))


if __name__ == "__main__":
    run()
