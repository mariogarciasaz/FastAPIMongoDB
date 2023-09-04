def productEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "category": item["category"],
        "price": item["price"],
        "stock": item["stock"],
    }
