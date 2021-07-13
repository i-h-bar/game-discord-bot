
from edge_functions.dice_logic.dice_groups import ALL_DICE
from utility_functions.strings import initialise

dice_map = {die.name: die() for die in ALL_DICE}

dice_map.update({key.lower(): value for key, value in dice_map.items()})
dice_map.update({initialise(key): value for key, value in dice_map.items()})
