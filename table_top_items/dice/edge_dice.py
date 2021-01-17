import re

from edge_functions.dice_logic.command_map import dice_map
from edge_functions.dice_logic.dice_roller import roll


async def roll_edge_dice(message):
    reply = f"{message.author.mention}"
    for dice_roll in message.content.split("+"):
        try:
            times = int(re.findall(r'\d+', dice_roll)[0])
        except IndexError:
            times = 1

        die = re.sub(r"[0-9]", "", dice_roll).strip().lower()

        if die not in list(dice_map.keys()):
            reply += "\nMeow"
        else:
            for key, value in dice_map.items():
                if key == die:
                    reply += f"\n`{value['dice name']}` = {roll(value['dice faces'], times)}"
                    break

    return reply
