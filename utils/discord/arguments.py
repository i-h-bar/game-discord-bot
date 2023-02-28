from utils.discord.argument import DiscordArgument


class Game(DiscordArgument, str):
    """Which game's commands you wish to get help with"""
    choices = {
        "World of Warcraft": "wow",
        "Magic the Gathering": "mtg",
        "Star Wars: Edge of the Empire": "sweote",
        "General": "general"
    }


class Hide(DiscordArgument, int):
    """Hide the dice roll Yes/No"""
    choices = {"Yes": True, "No": False}


class SpellItem(DiscordArgument, str):
    """Item or Spell to search (Fuzzy matches)"""


class Item(DiscordArgument, str):
    """Item to get (Fuzzy matches so don't worry if you mistype)"""


class Spell(DiscordArgument, str):
    """Spell to get (Fuzzy matches so don't worry if you mistype)"""


class Dice(DiscordArgument, str):
    """Size and number of dice to roll"""


class Expression(DiscordArgument, str):
    """Expression to calculate"""


class Flips(DiscordArgument, str):
    """Number of times to flip the coin"""


class Face(DiscordArgument, str):
    """The loss condition"""
    choices = {"Heads": "Heads", "Tails": "Tails"}


class WithThumb(DiscordArgument,  int):
    """Use the Karak's Thumb rules in determining the coin flips"""
    choices = {"Yes": True, "No": False}


class Card(DiscordArgument, str):
    """Card name to search"""
