import asyncpg
from config import DATABASE_URL


async def create_db_pool():
    return await asyncpg.create_pool(DATABASE_URL)

USER_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100),
    user_type VARCHAR(10)  -- "student" yoki "owner"
    user_id INTEGER REFERENCES users(id),
);
"""

HOUSING_TABLE = """
CREATE TABLE IF NOT EXISTS housings (
    id SERIAL PRIMARY KEY,
    description TEXT,
    price INTEGER,
    location VARCHAR(100),
    duration INTEGER,
    available BOOLEAN DEFAULT TRUE
);
"""

APPLICATION_TABLE = """
CREATE TABLE IF NOT EXISTS applications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    housing_id INTEGER REFERENCES housings(id),
    status VARCHAR(10) DEFAULT 'pending'  -- "accepted", "rejected"
);
"""


async def initialize_database(pool):
    async with pool.acquire() as connection:
        await connection.execute(USER_TABLE)
        await connection.execute(HOUSING_TABLE)
        await connection.execute(APPLICATION_TABLE)


