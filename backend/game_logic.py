DEFAULT_USER = {
    "hp": 100,
    "max_hp": 100,
    "attack": 10,
    "defense": 5,
    "level": 1,
    "gold": 0,
    "location": "Город",
    "inventory": {},
    "log": []
}

LOCATIONS = {
    "Город": {
        "name": "Город",
        "actions": ["Отдохнуть", "Выйти в лес", "В шахту", "Продать ресурсы"]
    },
    "Лес": {
        "name": "Лес",
        "actions": ["Сражаться", "Собирать ягоды", "Вернуться в город"]
    },
    "Шахта": {
        "name": "Шахта",
        "actions": ["Добывать руду", "Вернуться в город"]
    }
}

def get_location_by_name(name):
    return LOCATIONS.get(name, LOCATIONS["Город"])

def handle_action(user, action):
    location = get_location_by_name(user["location"])
    if action == "Отдохнуть":
        user["hp"] = user["max_hp"]
        return "Вы восстановили здоровье."
    elif action == "Выйти в лес":
        user["location"] = "Лес"
        return "Вы отправились в лес."
    elif action == "В шахту":
        user["location"] = "Шахта"
        return "Вы пошли в шахту."
    elif action == "Вернуться в город":
        user["location"] = "Город"
        return "Вы вернулись в город."
    elif action == "Сражаться":
        user["hp"] -= 10
        user["gold"] += 5
        return "Вы сражались с монстром и заработали 5 золота."
    elif action == "Собирать ягоды":
        user["inventory"].setdefault("Ягоды", 0)
        user["inventory"]["Ягоды"] += 3
        return "Вы собрали 3 ягоды."
    elif action == "Добывать руду":
        user["inventory"].setdefault("Руда", 0)
        user["inventory"]["Руда"] += 2
        return "Вы добыли 2 руды."
    elif action == "Продать ресурсы":
        berries = user["inventory"].get("Ягоды", 0)
        ore = user["inventory"].get("Руда", 0)
        earnings = berries * 1 + ore * 3
        user["gold"] += earnings
        user["inventory"]["Ягоды"] = 0
        user["inventory"]["Руда"] = 0
        return f"Вы продали ресурсы и получили {earnings} золота."
    return "Ничего не произошло."
