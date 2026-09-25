
def get_users(database: dict):
    return database.get("users")


def get_user(database: dict, user_id: int):
    users = database.get("users")
    return users.get(user_id)


def create_user(
    database: dict,
    id: int,
    name: str,
    password: str,
    roles: list[str]
):
    user_exists = database["users"].get(id) is not None
    if user_exists:
        return None

    user = {
        "id": id,
        "name": name,
        "password": password,
        "roles": roles,
    }

    database["users"][id] = user
    return user


def update_user_roles(
    database: dict,
    user: dict,
    roles: list[str]
):
    database["users"][user["id"]]["roles"] = roles
    return database["users"][user["id"]]


def update_user(
    database: dict,
    user: dict, 
    fields: dict,
):
    missing_fields = set(fields) - set(user)
    if missing_fields:
        raise ValueError(f"Non-existent fields: {missing_fields}")

    for field, value in fields.items():
        database["users"][user["id"]][field] = value

    return database["users"][user["id"]]


def delete_user(database: dict, user: dict):
    database["users"].pop(user["id"])
    return
