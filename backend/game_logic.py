# backend/game_logic.py

import random

# Базовые локации
LOCATIONS = {
    "forest": {
        "name": "Лес",
        "enemies": ["Гоблин", "Волк"],
        "resources": ["Дерево"],
    },
    "mine": {
        "name": "Шахта",
        "enemies": ["Крыса", "Зомби"],
        "resources": ["Камень", "Железо"],
    },
    "town": {
        "name": "Город",
        "enemies": [],
        "resources": [],
    }
}

# Получить текущую локацию
def get_location(location_id: str):
    return LOCATIONS.get(location_id, LOCATIONS["town"])

# Генерация врага
def generate_enemy(location: dict) -> dict | None:
    if location["enemies"]:
        name = random.choice(location["enemies"])
        hp = random.randint(5, 15)
        return {"name": name, "hp": hp}
    return None

# Боевая система
def fight(player: dict, enemy: dict) -> tuple[str, dict]:
    log = ""
    while player["hp"] > 0 and enemy["hp"] > 0:
        damage = random.randint(1, player["attack"])
        enemy["hp"] -= damage
        log += f"Вы нанесли {damage} урона врагу ({enemy['name']}).\n"

        if enemy["hp"] <= 0:
            log += f"Вы победили врага: {enemy['name']}!\n"
            break

        enemy_damage = random.randint(1, 4)
        player["hp"] -= enemy_damage
        log += f"Враг {enemy['name']} нанес {enemy_damage} урона вам.\n"

    return log, player

# Добыча ресурсов
def gather_resource(location: dict) -> str:
    if location["resources"]:
        resource = random.choice(location["resources"])
        amount = random.randint(1, 3)
        return f"Вы собрали {amount} x {resource}"
    return "Здесь нечего добывать."

# Прокачка характеристик
def upgrade_stat(player: dict, stat: str) -> str:
    if player["points"] > 0:
        player[stat] += 1
        player["points"] -= 1
        return f"{stat.capitalize()} увеличено!"
    return "Недостаточно очков навыков."
