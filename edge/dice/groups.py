import inspect

from edge.dice import definitions

ALL_DICE = [die for _, die in inspect.getmembers(definitions) if inspect.isclass(die) and hasattr(die, "name")]
