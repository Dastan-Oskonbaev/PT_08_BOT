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

    def connect(self):
        self.pool = asyncpg.create_pool(
            user=self.user,
            password=self.password,
            database=self.database,
            host=self.host,
            port=self.port
        )

    def disconnect(self):
        self.pool.close()



db = Database(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_DATABASE'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT'))
)