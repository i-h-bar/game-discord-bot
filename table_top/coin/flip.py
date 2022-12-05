import random

from table_top.coin.probibility_distribution import single_scenarios, thumb_scenarios

faces = "Heads", "Tails"

failure_face = {
    "Heads": "Tails",
    "Tails": "Heads"
}


async def flip_coin(number_of_flips: str):
    reply = ""

    try:
        times = int(number_of_flips)
    except ValueError:
        times = 1

    for _ in range(times):
        reply += f"\n`{random.choice(faces)}`"

    return reply


def flip_coin_until(face: str, with_thumb: int | None):
    if with_thumb:
        wins = random.choice(thumb_scenarios)
        winning_flips = ", ".join(f"`({face}`, `{random.choice(faces)}`)" for _ in range(wins))
        failure_flip = f"{', ' if wins > 0 else ''}(`{failure_face[face]}`, `{failure_face[face]}`)"
        message = f"Wins = `{wins}` - {winning_flips}{failure_flip}"

    else:
        wins = random.choice(single_scenarios)
        winning_flips = ", ".join(f"`{face}`" for _ in range(wins))
        failure_flip = f"{', ' if wins > 0 else ''}`{failure_face[face]}`"
        message = f"Wins = `{wins}` - {winning_flips}{failure_flip}"

    return message
