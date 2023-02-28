import inspect
from typing import Callable

from discord import app_commands
from discord.ext import commands

from utils.database import db
from utils.discord.models import DiscordArgument


class Bot(commands.Bot):
    def slash_command(self, alias: str | Callable = None):
        if inspect.iscoroutinefunction(alias):
            return self._alter_function(alias, alias.__name__)
        else:
            def wrapper(func):
                nonlocal alias
                return self._alter_function(func, alias)

            return wrapper

    def _alter_function(self, func, name):
        description = inspect.getdoc(func)
        spec = inspect.getfullargspec(func)
        sig = inspect.signature(func)
        params = dict(sig.parameters)

        for key, value in params.items():
            if issubclass(spec.annotations[key], DiscordArgument):

                value = inspect.Parameter(
                    value.name, value.kind, default=value.default, annotation=spec.annotations[key].annotation()
                )
                params[key] = value

        slash_command_args = {key: spec.annotations[key] for key in spec.args[1:]}

        func = app_commands.describe(
            **{
                arg: model.__doc__ for arg, model in slash_command_args.items()
            }
        )(func)

        choices = {
            arg: [app_commands.Choice(name=name, value=value) for name, value in info.choices.items()]
            for arg, info in slash_command_args.items() if info.choices
        }
        func = app_commands.choices(**choices)(func)

        sig = sig.replace(parameters=list(params.values()))
        func.__signature__ = sig

        func = self.tree.command(name=name, description=description)(func)

        return func

    class SlashCommand:
        def __init__(self, alias: str = None):
            self.alias = alias

        def __call__(self, func):
            name = self.alias or func.__name__

    async def close(self):
        await db.close()
        await super().close()
        print("Bot Closed Down")
