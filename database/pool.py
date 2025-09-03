import asyncpg
from contextlib import asynccontextmanager
from config import DATABASE_DSN

class DatabasePool:
    """Constructor sets pool to None to later initialize in asynchronously"""
    def __init__(self):
        self.pool = None
    
    async def init_pool(self):
        """Pool initialization"""
        try:
            self.pool = await asyncpg.create_pool(
                dsn=DATABASE_DSN,
                min_size=1,      # min number of connections
                max_size=10,     # max number of connections
                max_queries=500, # max number of queries
                max_inactive_connection_lifetime=300,  # 5 min
                timeout=30       # connection timeout
            )
        except Exception as e:
            print(f"Error creating connection pool: {e}")
    
    @asynccontextmanager
    async def acquire(self):
        """Context manager to acquire DB connection"""
        if self.pool is None:
            await self.init_pool()
            # Check again if setup failed
            if self.pool is None:
                    raise RuntimeError("Database pool could not be initialized.")
        
        async with self.pool.acquire() as connection:
            yield connection
    
    async def close(self):
        """Закрытие пула"""
        if self.pool:
            await self.pool.close()

# DB pool is now gloabal variable
db_pool = DatabasePool()