import random

from edge.dice.sides import BLANK, SUCCESS, ADVANTAGE, FAILURE, THREAT, TRIUMPH, DESPAIR, DARK, LIGHT


class EdgeDie:
    sides: tuple

    def __call__(self):
        return random.choice(self.sides)


class Boost(EdgeDie):
    name = "Boost Die"
    positive = True
    sides = (BLANK, BLANK, SUCCESS, SUCCESS + ADVANTAGE, ADVANTAGE * 2, ADVANTAGE)


class SetBack(EdgeDie):
    name = "Setback Die"
    positive = False
    sides = (BLANK, BLANK, FAILURE, FAILURE, THREAT, THREAT)


class Ability(EdgeDie):
    name = "Ability Die"
    positive = True
    sides = (BLANK, SUCCESS, SUCCESS, SUCCESS * 2, ADVANTAGE, ADVANTAGE, SUCCESS + ADVANTAGE, ADVANTAGE * 2)


class Difficulty(EdgeDie):
    name = "Difficulty Die"
    positive = False
    sides = (BLANK, FAILURE, FAILURE * 2, THREAT, THREAT, THREAT, THREAT * 2, FAILURE + THREAT)


class Proficiency(EdgeDie):
    name = "Proficiency Die"
    positive = True
    sides = (
        BLANK, SUCCESS, SUCCESS, SUCCESS * 2, SUCCESS * 2, ADVANTAGE, TRIUMPH, ADVANTAGE * 2,
        ADVANTAGE * 2, SUCCESS + ADVANTAGE, SUCCESS + ADVANTAGE, SUCCESS + ADVANTAGE
    )


class Challenge(EdgeDie):
    name = "Challenge Die"
    positive = False
    sides = (
        FAILURE, FAILURE, FAILURE * 2, FAILURE * 2, THREAT, THREAT,
        FAILURE + THREAT, FAILURE + THREAT, THREAT * 2, THREAT * 2, DESPAIR, BLANK
    )


class Force(EdgeDie):
    name = "Force Die"
    positive = None
    sides = (DARK, DARK, DARK, DARK, DARK, DARK, DARK * 2, LIGHT, LIGHT, LIGHT * 2, LIGHT * 2, LIGHT * 2)
