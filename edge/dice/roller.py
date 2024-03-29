import re
from collections import defaultdict

from edge.dice.command_map import dice_map
from edge.dice.groups import ALL_DICE
from edge.dice.sides import SUCCESS, ADVANTAGE, TRIUMPH, FAILURE, THREAT, DESPAIR, LIGHT, DARK, \
    BLANK


def roll_edge_dice(dice_command: str) -> str:
    reply = ""

    dice_rolls = defaultdict(list)
    for dice_roll in dice_command.split("+"):
        try:
            times = int(re.findall(r'\d+', dice_roll)[0])
        except IndexError:
            times = 1

        die = re.sub(r"[0-9]", "", dice_roll).strip().lower()

        try:
            die = dice_map[die]
        except KeyError:
            return f"The die '{die}' was not found in the dice bag :("
        else:
            for _ in range(times):
                dice_rolls[die.name].append(die())

    for key, value in dice_rolls.items():
        reply += f"\n`{key}` = {', '.join(value)}"

    reply += parse_edge_rolls(dice_rolls)

    return reply


def parse_edge_rolls(dice_rolls: dict[str, list[str]]) -> str:
    totals = defaultdict(int)

    for die in ALL_DICE:
        for rolls in dice_rolls.get(die.name, []):
            for roll in rolls:
                if die.positive is True:
                    totals[SUCCESS] += roll.count(SUCCESS)
                    totals[ADVANTAGE] += roll.count(ADVANTAGE)
                    totals[TRIUMPH] += roll.count(TRIUMPH)
                elif die.positive is False:
                    totals[FAILURE] += roll.count(FAILURE)
                    totals[THREAT] += roll.count(THREAT)
                    totals[DESPAIR] += roll.count(DESPAIR)
                else:
                    totals[LIGHT] += roll.count(LIGHT)
                    totals[DARK] += roll.count(DARK)

    success = (totals[SUCCESS] + totals[TRIUMPH]) - (totals[FAILURE] + totals[DESPAIR])
    advantage = totals[ADVANTAGE] - totals[THREAT]

    message = "\n`Total` = "
    for roll_info in [(success, SUCCESS, FAILURE), (advantage, ADVANTAGE, THREAT)]:
        message += format_message(*roll_info)

    if totals[LIGHT] > 0:
        message += f"{totals[LIGHT]}{LIGHT}, "
    if totals[DARK] > 0:
        message += f"{totals[DARK]}{DARK}, "

    if totals[TRIUMPH] > 0:
        message += f"{totals[TRIUMPH]}{TRIUMPH}, "
    if totals[DESPAIR] > 0:
        message += f"{totals[DESPAIR]}{DESPAIR}, "

    if message == "\n`Total` = ":
        message += f"{BLANK}"

    return message.rstrip(", ").replace("1", "")


def format_message(num, positive, negative):
    if num < 0:
        return f"{-num}{negative}, "
    elif num > 0:
        return f"{num}{positive}, "
    else:
        return ""
