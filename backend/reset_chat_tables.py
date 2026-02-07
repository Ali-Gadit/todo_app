import asyncio
import os
import sys
from sqlalchemy import text

# Add backend/src to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from src.db import engine, init_db

async def main():
    print("Resetting chat tables...")
    async with engine.begin() as conn:
        # Drop dependent table first
        await conn.execute(text("DROP TABLE IF EXISTS message CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS conversation CASCADE"))
    
    print("Re-creating tables...")
    await init_db()
    print("Tables reset and re-created successfully.")

if __name__ == "__main__":
    asyncio.run(main())
