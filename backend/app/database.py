from functools import lru_cache

database = {"users": {}}


@lru_cache
def get_db():
    return database
