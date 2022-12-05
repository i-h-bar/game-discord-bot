from utils.database import db
from wow.data.items import item_starting_letter_groups, normalised_items
from wow.matching import wow_fuzzy_match, make_url


async def item_look_up(item_name: str) -> tuple[bytes, str, str]:
    matched_id, matched_name, _ = await wow_fuzzy_match(item_name, item_starting_letter_groups, normalised_items)

    return await db.tooltip_from_item_id(matched_id), make_url(matched_id, matched_name, "item"), matched_name
