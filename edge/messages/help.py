from edge.dice import sides as ds

ROLLING_HELP = "To roll a die, type \"/r\" followed by any of the following:\n" \
               "Boost Die = bd\n" \
               "Set Back Die = sd\n" \
               "Difficulty Die = dd\n" \
               "Proficiency Die = pd\n" \
               "Challenge Die = cd\n" \
               "Force Die = fd\n" \
               "Ability Die = ad\n" \
               "\nTo roll more than one of the same die put a number before your die \"/r 3fd\"" \
               "\nTo roll more than one of a differing dice_legacy separate them by a \"+\" \"/r 2ad + 6sb\""

DICE_HELP = f"Success = {ds.SUCCESS}\n" \
            f"Fail = {ds.FAILURE}\n" \
            f"Triumph = {ds.TRIUMPH}\n" \
            f"Advantage = {ds.ADVANTAGE}\n" \
            f"Despair = {ds.DESPAIR}\n" \
            f"Threat = {ds.THREAT}\n" \
            f"Light = {ds.LIGHT}\n" \
            f"Dark = {ds.DARK}\n" \
            f"Blank = {ds.BLANK}"

EDGE_HELP = f"{ROLLING_HELP}\n{DICE_HELP}"
