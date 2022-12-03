import random

faces = "heads", "tales"


async def flip_coin(number_of_flips: str):
    reply = ""

    try:
        times = int(number_of_flips)
    except ValueError:
        times = 1

    for _ in range(times):
        reply += f"\n`{random.choice(faces)}`"

    return reply
