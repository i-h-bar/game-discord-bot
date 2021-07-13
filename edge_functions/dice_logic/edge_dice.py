import random

from edge_functions.dice_logic.dice_sides import BLANK, SUCCESS, ADVANTAGE, FAILURE, THREAT, TRIUMPH, DESPAIR, DARK, \
    LIGHT


class EdgeDie:
    sides = []

    def __call__(self):
        return random.choice(self.sides)


class Boost(EdgeDie):
    name = "Boost Die"
    sides = [BLANK, BLANK, SUCCESS, SUCCESS + ADVANTAGE, ADVANTAGE * 2, ADVANTAGE]


class SetBack(EdgeDie):
    name = "Setback Die"
    sides = [BLANK] * 2 + [FAILURE] * 2 + [THREAT] * 2


class Ability(EdgeDie):
    name = "Ability Die"
    sides = [
        BLANK, SUCCESS, SUCCESS, SUCCESS * 2, ADVANTAGE, ADVANTAGE, SUCCESS + ADVANTAGE, ADVANTAGE * 2
    ]


class Difficulty(EdgeDie):
    name = "Difficulty Die"
    sides = [BLANK, FAILURE, FAILURE * 2] + [THREAT] * 3 + [THREAT * 2, FAILURE + THREAT]


class Proficiency(EdgeDie):
    name = "Proficiency Die"
    sides = [BLANK, SUCCESS, SUCCESS, SUCCESS * 2, SUCCESS * 2, ADVANTAGE, TRIUMPH, ADVANTAGE * 2, ADVANTAGE * 2] + [
        SUCCESS + ADVANTAGE] * 3


class Challenge(EdgeDie):
    name = "Challenge Die"
    sides = [
        FAILURE, FAILURE, FAILURE * 2, FAILURE * 2, THREAT, THREAT,
        FAILURE + THREAT, FAILURE + THREAT, THREAT * 2, THREAT * 2, DESPAIR
    ]


class Force(EdgeDie):
    name = "Force Die"
    sides = [DARK]*6 + [DARK*2] + [LIGHT]*2 + [LIGHT*2]*3
