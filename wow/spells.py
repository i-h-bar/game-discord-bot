from utils.database import db
from wow.data.spells import normalised_spells, spell_starting_letter_groups
from wow.matching import wow_fuzzy_match, make_url


async def spell_look_up(spell_name: str) -> tuple[bytes, str, str]:
    matched_id, matched_name, _ = await wow_fuzzy_match(
        spell_name, await spell_starting_letter_groups(), await normalised_spells()
    )

    return await db.tooltip_from_spell_id(matched_id), make_url(matched_id, matched_name, "spell"), matched_name
