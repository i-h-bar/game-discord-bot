from edge_functions.dice_logic.command_map import dice_map
from table_top_items.dice.classic_dice_roller import roll_dice
from table_top_items.dice.edge_dice_roller import roll_edge_dice


def get_roll(message):
    content = message.content

    for key in dice_map.keys():
        if key in content:
            return roll_edge_dice(message)
    else:
        return roll_dice(message)
