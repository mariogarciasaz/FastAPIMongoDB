def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "username": item["username"],
        "name": item["name"],
        "email": item["email"],
        "disabled": item["disabled"],
        "role": item["role"]
    }
