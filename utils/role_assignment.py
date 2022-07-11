import re
import discord
from discord import RawReactionActionEvent, User


async def assign_from_reaction(reaction: RawReactionActionEvent):
    role = discord.utils.get(reaction.member.guild.roles, name=re.sub(r"[\d~]+", "", reaction.emoji.name.title()))
    if role is not None:
        await reaction.member.add_roles(role)


async def remove_from_reaction(reaction: RawReactionActionEvent, user: User):
    if (role := discord.utils.get(user.guild.roles, name=reaction.emoji.name.title())) is not None:
        await reaction.member.remove_roles(role)
