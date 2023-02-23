import re

from typing import Any


class DiscordArgument(Any):
    description: str = None
    annotation: type = str
    choices: dict[str, Any] | None = None


class Game(DiscordArgument):
    description = "Which game's commands you wish to get help with"
    choices = {
        "World of Warcraft": "wow",
        "Magic the Gathering": "mtg",
        "Star Wars: Edge of the Empire": "sweote",
        "General": "general"
    }


class Hide(DiscordArgument):
    description = "Hide the dice roll Yes/No"
    annotation = int
    choices = {"Yes": True, "No": False}


class SpellItem(DiscordArgument):
    description = "Item or Spell to search (Fuzzy matches)"


class Item(DiscordArgument):
    description = "Item to get (Fuzzy matches so don't worry if you mistype)"


class Spell(DiscordArgument):
    description = "Spell to get (Fuzzy matches so don't worry if you mistype)"


class Dice(DiscordArgument):
    description = "Size and number of dice to roll"


class Expression(DiscordArgument):
    description = "Expression to calculate"


class Flips(DiscordArgument):
    description = "Number of times to flip the coin"


class Face(DiscordArgument):
    description = "The loss condition"
    choices = {"Heads": "Heads", "Tails": "Tails"}


class WithThumb(DiscordArgument):
    description = "Use the Karak's Thumb rules in determining the coin flips"
    annotation = int
    choices = {"Yes": True, "No": False}


class Card(DiscordArgument):
    description = "Card name to search"
