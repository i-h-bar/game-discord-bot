import os

import asyncpg
from asyncpg import Connection

from wow.data.queries import WoWQueries


class DB(WoWQueries):
    def __init__(self):
        self.connection: Connection | None = None

    async def connect(self):
        self.connection = await asyncpg.connect(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("GAME_BOT_DB")
        )

    async def close(self):
        await self.connection.close()


db = DB()
