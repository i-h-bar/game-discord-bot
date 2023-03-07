import logging
import time
from collections import defaultdict
from datetime import datetime

import discord
import pytz
from discord.ext.commands import Context

from utils.aio.wrappers import preserve_sig
from utils.discord.types import Interaction
from utils.maths import round_down

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

requests = defaultdict(lambda: defaultdict(int))

interaction_kwargs = {"ephemeral": True}
context_kwargs = {}


def usage_logger(func):
    @preserve_sig(func)
    async def wrapper(*args, **kwargs):
        if isinstance(args[0], Context):
            interaction: Context = args[0]
            user = interaction.author
            send = interaction.send
            send_kwargs = context_kwargs
        else:
            interaction: Interaction = args[0]
            user = interaction.user
            send = interaction.response.send_message
            send_kwargs = interaction_kwargs

        time_section = round_down(time.time())
        requests[user.id][time_section] += 1

        if requests[user.id][time_section] < 60:
            logging.info(
                "\033[95m%s \033[94m%s (%s): \033[92m%s(%s) \033[93m(Request Count: %s)\033[0m",
                datetime.now(tz=pytz.UTC),
                user,
                interaction.guild.name,
                func.__name__,
                ', '.join(f'{k}={v}' for k, v in kwargs.items()),
                requests[user.id][time_section]
            )

            await func(*args, **kwargs)

        elif 60 <= requests[user.id][time_section] < 120:
            logging.warning(
                "\033[95m%s \033[94m%s (%s) \033[93mmade too many requests (%s)\033[0m",
                datetime.now(tz=pytz.UTC),
                user,
                interaction.guild.name,
                requests[user.id][time_section]
            )
            await send(
                "You have made too many requests to the bot within a time limit please try again later", **send_kwargs
            )
        else:
            logging.warning(
                "\033[95m%s \033[94m%s (%s) \033[93mmade too many requests (%s)\033[0m",
                datetime.now(tz=pytz.UTC),
                user,
                interaction.guild.name,
                requests[user.id][time_section]
            )

            return

        if len(requests[user.id]) > 1:
            del requests[user.id][tuple(requests[user.id].keys())[0]]

    return wrapper
