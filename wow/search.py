from utils.database import db
from wow.data.items import item_starting_letter_groups, normalised_items
from wow.data.spells import spell_starting_letter_groups, normalised_spells
from wow.matching import wow_fuzzy_match, make_url


async def look_up(name: str) -> tuple[bytes, str, str]:
    matched_item_id, matched_item_name, item_score = await wow_fuzzy_match(
        name, item_starting_letter_groups, normalised_items
    )
    matched_spell_id, matched_spell_name, spell_score = await wow_fuzzy_match(
        name, spell_starting_letter_groups, normalised_spells
    )

    if item_score >= spell_score:
        return (
            await db.tooltip_from_item_id(matched_item_id),
            make_url(matched_item_id, matched_item_name, "item"),
            matched_item_name
        )

    else:
        return (
            await db.tooltip_from_spell_id(matched_spell_id),
            make_url(matched_spell_id, matched_spell_name, "spell"),
            matched_spell_name
        )
