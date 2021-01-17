from utility_functions.numbers import ordinal


async def get_spell_level_and_school(level, school):
    if level == 0:
        return f"{school} cantrip".capitalize()
    else:
        return f"{await ordinal(level)}-level {school}".capitalize()
