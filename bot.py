import asyncio
import io
import os

import discord
from discord import Message, RawReactionActionEvent, DMChannel
from discord.ext import commands

from dnd.api import get_spell
from dnd.formatting.message import format_spell
from edge.messages.help import EDGE_HELP
from mtg.scryfall import search_scryfall
from table_top.calculator import calculate_from_message
from table_top.coin import flip_coin
from table_top.roller import get_roll
from utils.database import db
from utils.dev.measurement import async_time_it
from utils.discord import determine_send_function
from utils.feedback import open_feedback_session, take_feedback, clear_expired_feedback_sessions
from utils.help import HELP_MESSAGE
from utils.role_assignment import assign_from_reaction
from wow.data.items import item_starting_letter_groups
from wow.data.spells import spell_starting_letter_groups
from wow.parse import wow_look_up
from wow.professions import professions_reply


class Bot(commands.Bot):
    async def close(self):
        await db.close()
        await super().close()
        print("Bot Closed Down")


bot = Bot(command_prefix="/")


@bot.event
async def on_ready():
    await db.connect()
    await item_starting_letter_groups()
    await spell_starting_letter_groups()
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
        async for tooltip, url, name in wow_look_up(message.content):
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
        reply, tooltips = await professions_reply(message)

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


@bot.event
async def on_member_join(member):
    await member.send("Welcome!")


def run():
    bot.run(os.getenv("game_bot_token"))


if __name__ == "__main__":
    run()
