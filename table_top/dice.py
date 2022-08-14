import random


class Dice:
    def __init__(
            self,
            num_dice: str,
            dice_type: str,
            keep_high: str = None,
            keep_low: str = None,
            great_weapon_fighting: str = None
    ):
        self.dice_type = int(dice_type)
        self.raw_num = num_dice
        self.num_dice = int(self.raw_num) if self.raw_num else 1

        if self.num_dice > 100:
            raise ValueError(f"Number of dice too high {self.num_dice}")

        self.keep_high = int(keep_high) if keep_high else None
        self.keep_low = int(keep_low) if keep_low else None
        self.great_weapon_fighting = bool(great_weapon_fighting)
        self.sign = 1

        if self.num_dice < 0:
            self.num_dice = -self.num_dice
            self.sign = -1

        self.results = []
        self.rejected_rolls = []

        self.roll()

    def __repr__(self):
        if self.keep_high:
            suffix = f"kh{self.keep_high}"
        elif self.keep_low:
            suffix = f"kl{self.keep_low}"
        elif self.great_weapon_fighting:
            suffix = "gwf"
        else:
            suffix = ""

        return f"{self.sign * self.num_dice}d{self.dice_type}{suffix}"

    def __str__(self):
        if self.keep_high or self.keep_low:
            return (
                f"([{', '.join(f'~~{num}~~' for num in self.rejected_rolls)}] "
                f"{' + '.join(str(num) for num in self.results)})"
            )
        elif self.great_weapon_fighting:
            formatted_rolls = ' + '.join(
                f'[~~{reject}~~, {roll}]' if reject else str(roll)
                for reject, roll in zip(self.rejected_rolls, self.results)
            )

            return f"({formatted_rolls})"
        else:
            return f"{'-' if self.sign == -1 else ''}({' + '.join(str(num) for num in self.results)})"

    def __radd__(self, other):
        if isinstance(other, Dice):
            return other.total + self.total
        elif isinstance(other, int):
            return other + self.total
        else:
            raise ValueError("Other must be Dice or int type to add.")

    @classmethod
    def from_message(cls, num, die, kh, kl, gwf):
        if kh:
            kh = kh.lstrip("kh")
        if kl:
            kl = kl.lstrip("kl")

        return cls(num, die, kh, kl, gwf)

    @property
    def total(self):
        return self.sign * sum(self.results)

    @property
    def raw(self):
        return f"{self.raw_num}d{self.dice_type}"

    def roll(self):
        rolls = sorted(random.randint(1, self.dice_type) for _ in range(self.num_dice))

        if self.keep_high:
            self.results = rolls[-self.keep_high:]
            self.rejected_rolls = rolls[:self.num_dice - self.keep_high]
        elif self.keep_low:
            self.results = rolls[:self.keep_low]
            self.rejected_rolls = rolls[-(self.num_dice - self.keep_low):]
        elif self.great_weapon_fighting:
            for roll in rolls:
                if roll > 2:
                    self.results.append(roll)
                    self.rejected_rolls.append(0)
                else:
                    self.results.append(random.randint(1, self.dice_type))
                    self.rejected_rolls.append(roll)
        else:
            self.results = rolls
