import asyncpg
import os

from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self, user, password, database, host='localhost', port=5432):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=self.user,
            password=self.password,
            database=self.database,
            host=self.host,
            port=self.port
        )

    async def disconnect(self):
        self.pool.close()


    async def check_user(self, tg_id):
        async with self.pool.acquire() as conn:
            user = await conn.fetchrow(
                """
                    SELECT id 
                    FROM users
                    WHERE tg_id=$1
                """, tg_id
            )
            return user


    async def add_user(self, tg_id, username):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO users (tg_id, username)
                VALUES ($1, $2)
                """, tg_id, username
            )

    async def add_users_profile(self, tg_id, age, gender, profession):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                    UPDATE users
                    SET age=$1, gender=$2, profession=$3
                    WHERE tg_id=$4
                """, int(age), gender, profession, tg_id
            )

db = Database(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_DATABASE'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT'))
)