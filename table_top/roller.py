import re

from edge.dice.command_map import dice_map
from edge.dice.roller import roll_edge_dice
from table_top.dice import Dice


def get_roll(message):
    content = message.content

    for key in dice_map.keys():
        if key in content:
            return roll_edge_dice(message)
    else:
        content = content.lstrip("/rol ")

        if "[" in content and "]" in content:
            message = '\n'.join(
                roll_classic(dice.lstrip('[').rstrip(']'))
                for group in content.split(",")
                for num, dice in re.findall(r'(\d+)(\[.*])', group.strip())
                for _ in range(int(num))
            )
            return f"\n{message}"

        else:
            return roll_classic(content)


def roll_classic(content):
    dice_pool = [
        int(dice) if dice.strip().isdigit() else Dice.from_message(dice) for dice in content.split("+")
    ]

    return (
        f"`{' + '.join(repr(dice) for dice in dice_pool)}` = "
        f"{' + '.join(str(dice) for dice in dice_pool)} = {sum(dice_pool)}"
    )
