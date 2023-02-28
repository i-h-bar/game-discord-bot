import os

import asyncpg

from wow.data.queries import WoWQueries


class DB(WoWQueries):
    def __init__(self):
        self.connection: asyncpg.Pool | None = None

    def __str__(self):
        return f"{self.__class__.__name__}({self.connection})"

    async def connect(self):
        self.connection = await asyncpg.create_pool(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("GAME_BOT_DB"),
            max_inactive_connection_lifetime=0
        )

    async def close(self):
        await self.connection.close()


db = DB()
