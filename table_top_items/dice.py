import re
import random

from discord.message import Message
from table_top_items import calculate


async def roll_dice(message: Message):
    channel = message.channel
    content = message.content.replace("/roll", "").replace("/r", "")
    expression = content
    reply = f"{message.author.mention} `{content.replace(' ', '')}` = "

    dice = re.findall(r"(:?\d+)?d(:?\d+)?(:?kh1)?(:?kl1)?", content)

    for die in dice:
        roll_info = parse_rolls(die)
        typed_die = f"{die[0]}d{die[1]}{die[2]}{die[3]}"
        expression = expression.replace(typed_die, roll_info["expression"], 1).strip()
        content = content.replace(typed_die, roll_info["content"], 1).strip()

    reply += f"{content} = {int(await calculate(expression))}"

    await channel.send(reply)


def format_kh1_kl1(return_dict: dict, numbers: list, display_number: int) -> dict:
    return_dict["content"] = "("
    found = False
    for num in numbers:
        if num != display_number or found:
            return_dict["content"] += f'~~{num}~~, '
        else:
            found = True
            return_dict["content"] += f"{num}, "

    return_dict["content"] = return_dict["content"][:-2] + ")"

    return return_dict


def parse_rolls(dice_info: tuple) -> dict:
    return_dict = {}
    numbers = []

    times, die_type, *_ = dice_info

    if not times:
        times = "1"

    for _ in range(int(times)):
        numbers.append(random.randint(1, int(die_type)))

    if dice_info[2]:
        max_number = max(numbers)
        return_dict["expression"] = "(" + str(max_number) + ")"
        return_dict = format_kh1_kl1(return_dict, numbers, max_number)

    elif dice_info[3]:
        min_number = min(numbers)
        return_dict["expression"] = "(" + str(min_number) + ")"
        return_dict = format_kh1_kl1(return_dict, numbers, min_number)

    else:
        return_dict["expression"] = ""
        for num in numbers:
            return_dict["expression"] += f"{num} + "

        return_dict["expression"] = "(" + return_dict["expression"][:-3] + ")"
        return_dict["content"] = return_dict['expression']

    return return_dict
