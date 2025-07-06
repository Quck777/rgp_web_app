import random
from fastapi import Request

# Локации
locations = {
    "forest": {
        "name": "Лес",
        "actions": ["Охота", "Сбор трав", "Рубка деревьев"],
        "resources": [
            {"name": "Дерево", "chance": 0.7, "category": "материалы"},
            {"name": "Ягоды", "chance": 0.5, "category": "еда"},
            {"name": "Мясо", "chance": 0.2, "category": "еда"},
        ]
    },
    "mine": {
        "name": "Шахта",
        "actions": ["Добыча руды", "Добыча камня"],
        "resources": [
            {"name": "Камень", "chance": 0.8, "category": "материалы"},
            {"name": "Железная руда", "chance": 0.5, "category": "материалы"},
            {"name": "Золото", "chance": 0.1, "category": "материалы"},
        ]
    },
    "town": {
        "name": "Город",
        "actions": ["Рынок", "Торговля"],
        "resources": []
    }
}

# Стартовая информация о пользователе
def init_user():
    return {
        "location": "forest",
        "stats": {
            "strength": 1,
            "agility": 1,
            "intelligence": 1
        },
        "inventory": [],
        "log": [],
        "gold": 0
    }

# Получение текущей локации
def get_current_location(session: Request) -> dict:
    user = session.session.get("user")
    if user:
        loc_key = user.get("location", "forest")
        return locations.get(loc_key, locations["forest"])
    return locations["forest"]

# Добавление записи в лог
def add_log(session: Request, message: str):
    if "user" in session.session:
        session.session["user"]["log"].insert(0, message)
        session.session.modified = True

# Сбор ресурсов
def gather_resources(location_key: str, session: Request):
    user = session.session.get("user")
    if not user:
        return

    location = locations.get(location_key)
    if not location:
        return

    found_resources = []

    for resource in location["resources"]:
        if random.random() < resource["chance"]:
            found_resources.append(resource)

    if found_resources:
        for res in found_resources:
            add_to_inventory(session, res["name"], res["category"])
            add_log(session, f"Вы нашли {res['name']} ({res['category']})!")
    else:
        add_log(session, "Ничего не найдено...")

# Добавление предмета в инвентарь
def add_to_inventory(session: Request, item_name: str, category: str):
    user = session.session["user"]
    inventory = user["inventory"]

    for item in inventory:
        if item["name"] == item_name:
            item["quantity"] += 1
            break
    else:
        inventory.append({"name": item_name, "quantity": 1, "category": category})

    session.session.modified = True

# Получение инвентаря по категориям
def get_inventory_by_category(session: Request):
    user = session.session.get("user", {})
    inventory = user.get("inventory", [])

    categorized = {}
    for item in inventory:
        category = item.get("category", "другое")
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(item)

    return categorized

# Удаление предмета из инвентаря
def remove_item(session: Request, item_name: str):
    user = session.session["user"]
    inventory = user["inventory"]

    for item in inventory:
        if item["name"] == item_name:
            item["quantity"] -= 1
            if item["quantity"] <= 0:
                inventory.remove(item)
            break

    session.session.modified = True

# Продажа предмета (1 предмет = 5 золота)
def sell_item(session: Request, item_name: str):
    user = session.session["user"]
    inventory = user["inventory"]

    for item in inventory:
        if item["name"] == item_name:
            user["gold"] += 5
            remove_item(session, item_name)
            add_log(session, f"Вы продали {item_name} за 5 золота!")
            break

    session.session.modified = True
