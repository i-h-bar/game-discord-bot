import inspect
from typing import Callable, Coroutine, Sequence, Any

from discord import app_commands
from discord.abc import Snowflake
from discord.ext import commands
from discord.utils import MISSING

from utils.aio.requests import client
from utils.database import db
from utils.discord.argument import DiscordArgument
from utils.discord.logging import usage_logger
from utils.discord.types import Interaction


class Bot(commands.Bot):
    def slash_command(
            self,
            alias: str | None = None,
            nsfw: bool = False,
            guild: int | None = MISSING,
            guilds: Sequence[Snowflake] | Sequence[int] = MISSING,
            auto_locale_strings: bool = True,
            extras: dict[Any, Any] = MISSING,
    ):
        def wrapper(func: Callable[[Interaction, ...], Coroutine]):
            spec = inspect.getfullargspec(func)
            command_params = {
                key: spec.annotations[key] for key in spec.args[1:]
                if issubclass(spec.annotations[key], DiscordArgument)
            }

            func = app_commands.describe(**{arg: model.__doc__ for arg, model in command_params.items()})(func)
            func = app_commands.choices(
                **{name: arg.formatted_choices() for name, arg in command_params.items() if arg.choices}
            )(func)
            func = app_commands.rename(
                **{name: arg.name for name, arg in command_params.items() if arg.name}
            )(func)

            func = usage_logger(func)

            return self.tree.command(
                name=alias or func.__name__,
                description=inspect.getdoc(func),
                nsfw=nsfw,
                guild=guild,
                guilds=guilds,
                auto_locale_strings=auto_locale_strings,
                extras=extras
            )(func)

        return wrapper

    async def close(self):
        await db.close()
        await client.__aexit__()
        await super().close()
        print("Bot Closed Down")
