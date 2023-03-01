import asyncio

import discord

from utils.aio.requests import client

header = {
    "referer": "https://classic.warcraftlogs.com"
}


async def search_character(name: str) -> str:
    response = await client.get(
        f"https://classic.warcraftlogs.com/search/autocomplete?term={name}", headers=header
    )

    return "\n".join(
        set(
            f"{result['label']} ({result['server']}): <{result['link']}>" for result in response.json()
            if result["type"] == "Character"
        )
    )


async def search_characters(user: discord.User) -> str:
    mutual_guilds_users = [member for guild in user.mutual_guilds for member in list(guild.members)]

    request_list = [
        user.name, *(member.nick for member in mutual_guilds_users if member.id == user.id and member.nick)
    ]

    responses = await asyncio.gather(
        *(client.get(
            f"https://classic.warcraftlogs.com/search/autocomplete?term={name}", headers=header
        ) for name in request_list)
    )
    characters = (result for response in responses for result in response.json())

    return "\n".join(
        set(
            f"{result['label']} ({result['server']}): <{result['link']}>" for result in characters
            if result["type"] == "Character"
        )
    )
