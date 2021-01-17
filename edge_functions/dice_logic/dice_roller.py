import random


def roll(die, times):
    rolls = []
    for i in range(times):
        rolls.append(random.choice(die))

    if len(rolls) == 1:
        return rolls[0]
    else:
        return " + ".join(rolls)
