import re

from discord import Message

from edge_functions.dice_logic.command_map import dice_map


async def roll_edge_dice(message: Message) -> str:
    reply = f"{message.author.mention}"

    for dice_roll in message.content.split("+"):
        try:
            times = int(re.findall(r'\d+', dice_roll)[0])
        except IndexError:
            times = 1

        die = re.sub(r"[0-9]", "", dice_roll).strip().lower()

        try:
            die = dice_map[die]
        except KeyError:
            reply += f" the die '{die}' was not found in the dice bag :("
        else:
            reply += f"\n`{die.name}` = {' + '.join([die() for _ in range(times)])}"

    return reply
