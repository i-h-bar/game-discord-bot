from edge_functions.dice_logic import dice_sides as ds

rolling_help = "To roll a die, type \"/r\" followed by any of the following:\n" \
               "Boost Die = bd\n" \
               "Set Back Die = sbd\n" \
               "Difficulty Die = dd\n" \
               "Proficiency Die = pd\n" \
               "Challenge Die = cd\n" \
               "Force Die = fd\n" \
               "\nTo roll more than one of the same die put a number before your die \"/r 3fd\"" \
               "\nTo roll more than one of a differing dice separate them by a \"+\" \"/r 2fd + 6sbd\""


dice_help = f"Success = {ds.success}\n" \
            f"Fail = {ds.fail}\n" \
            f"Triumph = {ds.triumph}\n" \
            f"Advantage = {ds.advantage}\n" \
            f"Despair = {ds.despair}\n" \
            f"Threat = {ds.threat}\n" \
            f"Light = {ds.light}\n" \
            f"Dark = {ds.dark}\n" \
            f"Blank = {ds.blank}"


edge_help = f"{rolling_help}\n{dice_help}"
