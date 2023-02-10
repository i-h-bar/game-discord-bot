from utils.database import db
from wow.data.spells_and_items import object_starting_letter_groups, normalised_objects
from wow.matching import wow_fuzzy_match, make_url


async def look_up(name: str) -> tuple[bytes, str, str]:
    matched_id, matched_name, table = await wow_fuzzy_match(
        name, await object_starting_letter_groups(), await normalised_objects()
    )

    if table == "item":
        return (
            await db.tooltip_from_item_id(matched_id),
            make_url(matched_id, matched_name, "item"),
            matched_name
        )

    else:
        return (
            await db.tooltip_from_spell_id(matched_id),
            make_url(matched_id, matched_name, "spell"),
            matched_name
        )
