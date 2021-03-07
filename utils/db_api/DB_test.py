import asyncio
import uuid
from random import randint


from utils.db_api.postgresql import Database

async def test():
    await db.create()
    print("creating database")
    await db.create_table_users()
    a = await db.get_all_users()
    print(a)
    print(int(1234.9))
    a = "1234124124321421412410 оптфыль ejgnlkdm"
    print(len(a))

db = Database()
asyncio.run(test())
