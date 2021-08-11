from edge.dice.command_map import dice_map
from edge.dice.roller import roll_edge_dice
from table_top.dice.classic import roll_dice


def get_roll(message):
    content = message.content

    for key in dice_map.keys():
        if key in content:
            return roll_edge_dice(message)
    else:
        return roll_dice(message)
