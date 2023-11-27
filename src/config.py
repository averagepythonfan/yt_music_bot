import os

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

ADMIN = os.getenv("ADMIN")
TOKEN = os.getenv("TOKEN")

REDIS_HOST: str = os.getenv("REDIS_HOST")
REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")