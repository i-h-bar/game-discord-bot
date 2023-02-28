import inspect
from typing import Callable, Coroutine, Sequence

from discord import app_commands
from discord.abc import Snowflake
from discord.ext import commands
from discord.utils import MISSING

from utils.database import db
from utils.discord.types import Integration


class Bot(commands.Bot):
    def slash_command(
            self,
            alias: str | None = None,
            nsfw: bool = False,
            guild: int | None = MISSING,
            guilds: Sequence[Snowflake] | Sequence[int] = MISSING
    ):
        def wrapper(func: Callable[[Integration, ...], Coroutine]):
            spec = inspect.getfullargspec(func)

            slash_command_args = {key: spec.annotations[key] for key in spec.args[1:]}
            func = app_commands.describe(**{arg: model.__doc__ for arg, model in slash_command_args.items()})(func)

            choices = {arg_name: arg.formatted_choices() for arg_name, arg in slash_command_args.items() if arg.choices}
            func = app_commands.choices(**choices)(func)

            func = self.tree.command(
                name=alias or func.__name__, description=inspect.getdoc(func), nsfw=nsfw, guild=guild, guilds=guilds
            )(func)

            return func

        return wrapper

    async def close(self):
        await db.close()
        await super().close()
        print("Bot Closed Down")
