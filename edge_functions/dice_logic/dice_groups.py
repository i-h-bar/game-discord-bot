import inspect

from edge_functions.dice_logic import edge_dice

ALL_DICE = [die for _, die in inspect.getmembers(edge_dice) if inspect.isclass(die) and hasattr(die, "name")]
