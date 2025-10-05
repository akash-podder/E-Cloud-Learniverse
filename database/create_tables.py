import asyncio
from database.database_init import init_models

asyncio.run(init_models())
