from typing import Callable, Awaitable

from discord import TextChannel, Message, VoiceChannel


def determine_send_function(message: Message):
    channel = message.channel

    if message.content.startswith("!DM") or isinstance(channel, VoiceChannel):
        message.content = message.content.lstrip("!DM ")
        return message.author.send
    elif message.content.startswith("!hide"):
        message.content = message.content.lstrip("!hide ")
        return send_hidden(channel)
    else:
        return channel.send


def send_hidden(channel: TextChannel) -> Callable[[str], Awaitable]:
    async def wrapper(message: str):
        await channel.send(f"||{message}||")

    return wrapper
