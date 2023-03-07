import io
import os

import discord

from edge.help_message import EDGE_HELP
from mtg.help_message import MTG_HELP
from mtg.scryfall import get_card
from table_top.calculator import calculate_from_message
from table_top.coin.flip import flip_coin_until, flip_coin
from table_top.help_message import GENERAL_HELP
from table_top.roller import get_roll
from utils.aio.requests import client
from utils.database import db
from utils.discord.arguments import Game, Hide, SpellItem, Item, Spell, Dice, Expression, Flips, Face, WithThumb, Card, \
    WCLName
from utils.discord.extended_bot import Bot
from utils.discord.types import Integration
from wow.data.items import item_starting_letter_groups
from wow.data.spells import spell_starting_letter_groups
from wow.data.spells_and_items import object_starting_letter_groups
from wow.help_message import WOW_HELP
from wow.items import item_look_up
from wow.search import look_up
from wow.spells import spell_look_up
from wow.wcl.characters import search_characters, search_character

bot = Bot(command_prefix="/", intents=discord.Intents.all())


@bot.event
async def on_ready():
    await db.connect()
    await client.__aenter__()
    await item_starting_letter_groups()
    await spell_starting_letter_groups()
    await object_starting_letter_groups()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Slash Commands"))
    print("id: ", bot.application_id)
    synced = await bot.tree.sync()

    print(f"Synced {len(synced)} commands")
    print("Game bot initialised")


@bot.slash_command(alias="help")
async def help_function(interaction: Integration, game: Game):
    """Get help with using the bot for a particular game."""
    if game == "wow":
        help_msg = WOW_HELP
    elif game == "mtg":
        help_msg = MTG_HELP
    elif game == "sweote":
        help_msg = EDGE_HELP
    else:
        help_msg = GENERAL_HELP

    return await interaction.response.send_message(help_msg, ephemeral=True)


@bot.slash_command()
async def search(interaction: Integration, name: SpellItem, hide: Hide = None):
    """Search from an Item or Spell in Wrath of the Lich King Classic (Fuzzy Matches)"""
    tooltip, url, name = await look_up(name)

    await interaction.response.send_message(
        f"<{url}>",
        file=discord.File(io.BytesIO(tooltip), f"{name}.png"),
        ephemeral=bool(hide)
    )


@bot.slash_command()
async def item(interaction: Integration, item_name: Item, hide: Hide = None):
    """Search for an item in Wrath of the Lich King Classic (Fuzzy Matches)"""
    tooltip, url, name = await item_look_up(item_name)

    await interaction.response.send_message(
        f"<{url}>",
        file=discord.File(io.BytesIO(tooltip), f"{name}.png"),
        ephemeral=bool(hide)
    )


@bot.slash_command()
async def spell(interaction: Integration, spell_name: Spell, hide: Hide = None):
    """Search for a spell in Wrath of the Lich King Classic (Fuzzy Matches)"""
    tooltip, url, name = await spell_look_up(spell_name)

    await interaction.response.send_message(
        f"<{url}>",
        file=discord.File(io.BytesIO(tooltip), f"{name}.png"),
        ephemeral=bool(hide)
    )


@bot.slash_command()
async def roll(interaction: Integration, dice: Dice, hide: Hide = None):
    """Roll any number/size of numerical or SW:EotE dice."""
    await interaction.response.send_message(get_roll(dice), ephemeral=bool(hide))


@bot.slash_command()
async def calc(interaction: Integration, expression: Expression):
    """Run a simple numerical calculation"""
    return await interaction.response.send_message(calculate_from_message(expression))


@bot.slash_command()
async def flip(interaction: Integration, number_of_flips: Flips):
    """Flip a coin x amount of times"""
    return await interaction.response.send_message(await flip_coin(number_of_flips))


@bot.slash_command()
async def flip_until(interaction: Integration, face: Face, with_thumb: WithThumb = None):
    """Keep flipping coins until a result is flipped"""
    return await interaction.response.send_message(flip_coin_until(face, with_thumb))


@bot.slash_command()
async def card(interaction: Integration, name: Card):
    """Search for a Magic the Gathering card (Fuzzy Matches)"""
    card_info, card_image = await get_card(name)
    return await interaction.response.send_message(
        file=discord.File(io.BytesIO(card_image), f"{card_info.get('name', 'default').replace(' ', '_')}.png")
    )


@bot.slash_command()
async def wcl(interaction: Integration, name: WCLName, hide: Hide = None):
    """Search for a user on Classic Warcraft Logs"""

    message = await search_character(name)

    if message:
        await interaction.response.send_message(message, ephemeral=bool(hide))
    else:
        await interaction.response.send_message(f"\"{name}\" does not match anything on WCLs :(", ephemeral=bool(hide))


@bot.tree.context_menu(name="Warcraft Logs")
async def wcl_user(interaction: Integration, user: discord.User):
    message = await search_characters(user)

    if message:
        await interaction.response.send_message(message, ephemeral=True)
    else:
        await interaction.response.send_message("Discord name does not match anything on WCLs :(", ephemeral=True)


@bot.tree.context_menu(name="Warcraft Logs")
async def wcl_message(interaction: Integration, message: discord.Message):
    message = await search_characters(message.author)

    if message:
        await interaction.response.send_message(message, ephemeral=True)
    else:
        await interaction.response.send_message("Discord name does not match anything on WCLs :(", ephemeral=True)


@bot.command(name="servers")
async def servers(ctx):
    await ctx.send(f"{len(bot.guilds)}")


def run():
    bot.run(os.getenv("game_bot_token"))


if __name__ == "__main__":
    run()
