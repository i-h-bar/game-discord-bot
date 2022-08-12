import asyncio
import io
import os

import discord
from discord import Message, RawReactionActionEvent, DMChannel
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
from utils.feedback import open_feedback_session, take_feedback, clear_expired_feedback_sessions
from utils.help import HELP_MESSAGE
from utils.role_assignment import assign_from_reaction
from wow.parse import item_look_up
from wow.professions import profession_map

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

    if isinstance(message.channel, DMChannel):
        await take_feedback(message)

    if message.content.startswith("!feedback"):
        await clear_expired_feedback_sessions()
        await open_feedback_session(message)

    elif not isinstance(message.channel, DMChannel) and "feedback-channel" in message.channel.name:
        await message.delete()

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

    elif "{{" in message.content and "}}" in message.content and not message.content.startswith("/who"):
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
        reply = ""
        professions, tooltips = await profession_map(message)

        if professions is None and tooltips is None:
            return

        for profession, wanted_items in professions.items():
            role = discord.utils.get(message.guild.roles, name=profession)
            if role is not None:
                reply += f"Hey there {role.mention} can you make [{', '.join(f'**{item.title()}**' for item in wanted_items)}] for {message.author.mention}\n"

        if "not prof crafted" in professions:
            reply += f"Sorry [{', '.join(f'**{item.title()}**' for item in professions['not prof crafted'])}] can't be crafted by a profession :("

        if reply:
            await send_message(reply)

        for tooltip, name in tooltips:
            await send_message(file=discord.File(io.BytesIO(tooltip), f"{name}.png"))

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
