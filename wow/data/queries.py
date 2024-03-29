from asyncpg import Connection


class WoWQueries:
    connection: Connection | None

    async def tooltip_from_item_id(self, item_id) -> bytes:
        return await self.connection.fetchval(
            f"select t.tooltip from item i join tooltip t on t.tooltip_id = i.tooltip_id and i.item_id = {item_id}"
        )

    async def tooltip_from_spell_id(self, spell_id) -> bytes:
        return await self.connection.fetchval(
            f"select t.tooltip from spell s join tooltip t on t.tooltip_id = s.tooltip_id and s.spell_id = {spell_id}"
        )

    async def all_items_ids_and_names(self):
        return await self.connection.fetch(f"select i.item_id, i.name from item i")

    async def all_spells_ids_and_names(self):
        return await self.connection.fetch(
            f"select spell_id, name from spell order by rank"
        )

    async def all_item_names(self):
        return await self.connection.fetch(f"select i.name from item i")
