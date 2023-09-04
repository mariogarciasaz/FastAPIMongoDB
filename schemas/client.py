def clientEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "lastname": item["lastname"],
        "address": item["address"],
        "phone": item["phone"],
        "email": item["email"],
    }
