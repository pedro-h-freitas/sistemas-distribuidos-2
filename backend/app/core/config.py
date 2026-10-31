import os

POSTGRES_USER = os.getenv(
    "POSTGRES_USER",
    "user",
)
POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD",
    "pass",
)
POSTGRES_HOST = os.getenv(
    "POSTGRES_HOST",
    "localhost",
)
POSTGRES_DB = os.getenv(
    "POSTGRES_DB",
    "db_example",
)
POSTGRES_PORT = os.getenv(
    "POSTGRES_PORT",
    "5435",
)
DATABASE_URL = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
