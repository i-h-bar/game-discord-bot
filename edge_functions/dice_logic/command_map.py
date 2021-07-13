import inspect

from edge_functions.dice_logic import edge_dice
from utility_functions.strings import initialise

dice_map = {
    die.name: die() for _, die in inspect.getmembers(edge_dice) if inspect.isclass(die) and hasattr(die, "name")
}

dice_map.update({key.lower(): value for key, value in dice_map.items()})
dice_map.update({initialise(key): value for key, value in dice_map.items()})
