from edge.dice.groups import ALL_DICE
from utils.strings import initialise

dice_map = {die.name: die() for die in ALL_DICE}

dice_map.update({key.lower(): value for key, value in dice_map.items()})
dice_map.update({initialise(key): value for key, value in dice_map.items()})
