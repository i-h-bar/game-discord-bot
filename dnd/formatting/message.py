from dnd.formatting.spell import get_spell_level_and_school

MAX_MESSAGE_LENGTH = 2000


async def format_spell(message, spell_name, spell_info):
    reply = f"{message.author.mention} `{spell_name}`\n"

    spell_description = '\n'.join(spell_info['desc'])
    materials = spell_info.get("material", "")
    if materials:
        materials = f"({materials.lower().rstrip('.')})"

    reply += f"**{spell_info['name']}** - \n"
    reply += f"*{await get_spell_level_and_school(spell_info['level'], spell_info['school']['name'])}* \n"
    reply += f"**Casting Time:** {spell_info['casting_time']} \n"
    reply += f"**Range:** {spell_info['range']} \n"
    reply += f"**Components:** {', '.join(spell_info['components'])} {materials} \n"
    reply += f"**Duration:** {'Concentration,' if spell_info['concentration'] else ''} {spell_info['duration']} \n"
    reply += f"**Classes:** {', '.join(_class['name'] for _class in spell_info['classes'])} \n"
    reply += f"{spell_description} \n"

    higher_level = spell_info.get("higher_level")
    if higher_level is not None:
        higher_level = '\n'.join(higher_level)
        reply += f"{higher_level} \n"

    return (reply[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(reply), MAX_MESSAGE_LENGTH))
