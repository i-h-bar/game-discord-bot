from edge_functions.dice_logic.command_map import dice_map
from table_top_items.dice.classic_dice_roller import roll_dice
from table_top_items.dice.edge_dice_roller import roll_edge_dice


async def get_roll(message):
    content = message.content

    for key in dice_map.keys():
        if key in content:
            return await roll_edge_dice(message)
    else:
        return await roll_dice(message)
