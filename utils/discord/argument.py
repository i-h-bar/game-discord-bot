from typing import Union

from discord import app_commands
from discord.app_commands.transformers import ALLOWED_DEFAULTS


ALLOWED_DEFAULTS = set(_type for tup in ALLOWED_DEFAULTS.values() for _type in tup)


class DiscordArgument:
    # __origin__ = Union
    choices: dict | None = None

    @classmethod
    def annotation(cls):
        for base in cls.__bases__:
            if DiscordArgument is not base and base in ALLOWED_DEFAULTS:
                return base
        else:
            return str

    @classmethod
    def formatted_choices(cls):
        return [app_commands.Choice(name=name, value=value) for name, value in cls.choices.items()]
