from __future__ import annotations

from discord import app_commands
from discord.app_commands.transformers import ALLOWED_DEFAULTS, BUILT_IN_TRANSFORMERS

ALLOWED_DEFAULTS_SET = set(_type for tup in ALLOWED_DEFAULTS.values() for _type in tup)


class _Transformer(type):
    def __init__(cls: DiscordArgument, name, bases, clsdict):
        for base in bases:
            if base in ALLOWED_DEFAULTS_SET:
                break
        else:
            base = str

        BUILT_IN_TRANSFORMERS[cls] = BUILT_IN_TRANSFORMERS[base]
        super().__init__(name, bases, clsdict)


class DiscordArgument(metaclass=_Transformer):
    name: str | None = None
    choices: dict | None = None

    @classmethod
    def formatted_choices(cls):
        return [app_commands.Choice(name=name, value=value) for name, value in cls.choices.items()]
