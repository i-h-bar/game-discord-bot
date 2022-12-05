import re

from edge.dice.command_map import dice_map
from edge.dice.roller import roll_edge_dice
from table_top.calculator import calculate, operators
from table_top.constants import DICE_REGEX
from table_top.dice import Dice


def get_roll(dice_command: str):
    if len(dice_command) > 100:
        raise ValueError("Content too large")

    for key in dice_map.keys():
        if key in dice_command:
            return roll_edge_dice(dice_command)
    else:
        if "[" in dice_command and "]" in dice_command:
            message = '\n'.join(
                roll_classic(dice.lstrip('[').rstrip(']'))
                for group in dice_command.split(",")
                for num, dice in re.findall(r'(\d+)(\[.*])', group.strip())
                for _ in range(int(num)) if int(num) < 51
            )

            if not message:
                raise ValueError("No dice groups were rolled")

            return f"\n{message}"

        else:
            return roll_classic(dice_command)


def roll_classic(content):
    calculation = content
    results = content

    for dice in (Dice.from_message(*dice) for dice in re.findall(DICE_REGEX, content)):
        written_dice = dice.raw
        calculation = re.sub(written_dice, str(dice.total), calculation, count=1)
        results = re.sub(written_dice, str(dice), results, count=1)

    return_string = f"`{content}` = {results} = {calculate(calculation)}"
    for operator in operators.keys():
        return_string = return_string.replace(operator, f" {operator} ").replace("  ", " ")

    return return_string
