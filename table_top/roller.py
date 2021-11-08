import re

from edge.dice.command_map import dice_map
from edge.dice.roller import roll_edge_dice
from table_top.constants import DICE_REGEX
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
    found_dice = [dice for dice in re.findall(DICE_REGEX, content.replace(" ", "")) if any(dice)]
    dice_pool = [
        int(dice[0]) if dice[0].lstrip("-").isdigit() and not dice[1]
        else Dice.from_message(*dice)
        for dice in found_dice
    ]

    return (
        f"`{' + '.join(repr(dice) for dice in dice_pool)}` = "
        f"{' + '.join(str(dice) for dice in dice_pool)} = {sum(dice_pool)}"
    ).replace("+ -", "- ")
