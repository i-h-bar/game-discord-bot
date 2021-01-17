from edge_functions.dice_logic import dice

dice_map = {
    "bd": 
        {"dice faces": dice.set_back_die, 
         "dice name": "Boost Die"},
    "boost die": 
        {"dice faces": dice.set_back_die, 
         "dice name": "Boost Die"},
    "set back die": 
        {"dice faces": dice.set_back_die, 
         "dice name": "Set Back Die"},
    "sbd": 
        {"dice faces": dice.set_back_die, 
         "dice name": "Set Back Die"},
    "ability die": 
        {"dice faces": dice.ability_die, 
         "dice name": "Ability Die"},
    "ad": 
        {"dice faces": dice.ability_die, 
         "dice name": "Ability Die"},
    "difficulty die": 
        {"dice faces": dice.difficulty_die, 
         "dice name": "Difficulty Die"},
    "dd": 
        {"dice faces": dice.difficulty_die, 
         "dice name": "Difficulty Die"},
    "proficiency die": 
        {"dice faces": dice.proficiency_die, 
         "dice name": "Proficiency Die"},
    "pd": 
        {"dice faces": dice.proficiency_die, 
         "dice name": "Proficiency Die"},
    "challenge die": 
        {"dice faces": dice.challenge_die, 
         "dice name": "Challenge Die"},
    "cd": 
        {"dice faces": dice.challenge_die, 
         "dice name": "Challenge Die"},
    "force die": 
        {"dice faces": dice.force_die, 
         "dice name": "Force Die"},
    "fd": 
        {"dice faces": dice.force_die, 
         "dice name": "Force Die"},
}
