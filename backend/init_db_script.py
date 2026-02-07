import asyncio
import os
import sys
from sqlalchemy import text

# Add backend/src to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from src.config import settings
from src.db import engine, init_db

async def main():
    print(f"DEBUG: Using DATABASE_URL: {settings.DATABASE_URL}")
    print("Forcing reset of chat tables...")
    async with engine.begin() as conn:
        # Drop tables to clear any invalid columns like 'thread_id'
        await conn.execute(text("DROP TABLE IF EXISTS message CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS conversation CASCADE"))
    
    print("Initializing database...")
    await init_db()
    print("Database reset successfully.")

if __name__ == "__main__":
    asyncio.run(main())