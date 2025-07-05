import random

MONSTERS = [
    {"name": "Гоблин", "hp": 20, "damage": 5, "exp": 10},
    {"name": "Орк", "hp": 30, "damage": 8, "exp": 15},
    {"name": "Волк", "hp": 25, "damage": 6, "exp": 12}
]

game_state = {
    "player": {
        "x": 2,
        "y": 2,
        "name": "Рыцарь",
        "hp": 100,
        "level": 1,
        "exp": 0
    },
    "map": [],
    "monsters": {},
    "log": ["Добро пожаловать в мир RPG!"]
}

def generate_map():
    types = ["Лес", "Гора", "Город", "Шахта"]
    game_state["map"] = [[random.choice(types) for _ in range(5)] for _ in range(5)]
    game_state["map"][2][2] = "Вы здесь"

    # Генерация монстров
    game_state["monsters"] = {}
    for _ in range(5):  # 5 монстров
        x, y = random.randint(0, 4), random.randint(0, 4)
        if (x, y) != (2, 2):
            game_state["monsters"][(x, y)] = random.choice(MONSTERS)

generate_map()

def move_player(direction):
    dx, dy = 0, 0
    if direction == "up":
        dx = -1
    elif direction == "down":
        dx = 1
    elif direction == "left":
        dy = -1
    elif direction == "right":
        dy = 1

    new_x = game_state["player"]["x"] + dx
    new_y = game_state["player"]["y"] + dy

    if 0 <= new_x < 5 and 0 <= new_y < 5:
        game_state["player"]["x"] = new_x
        game_state["player"]["y"] = new_y
        return resolve_cell(new_x, new_y)
    else:
        game_state["log"].insert(0, "Нельзя идти туда!")
        return "Стена!"

def resolve_cell(x, y):
    if (x, y) in game_state["monsters"]:
        monster = game_state["monsters"].pop((x, y))
        return combat(monster)
    else:
        location = game_state["map"][x][y]
        game_state["log"].insert(0, f"Вы перешли в: {location}")
        return f"Перемещено в {location}"

def combat(monster):
    log = []
    player = game_state["player"]
    log.append(f"Вы встретили монстра: {monster['name']}!")

    while monster["hp"] > 0 and player["hp"] > 0:
        # Игрок атакует
        dmg = random.randint(8, 15)
        monster["hp"] -= dmg
        log.append(f"Вы ударили {monster['name']} на {dmg} урона.")

        if monster["hp"] <= 0:
            log.append(f"{monster['name']} повержен!")
            player["exp"] += monster["exp"]
            level_check()
            break

        # Монстр атакует
        dmg = random.randint(monster["damage"] - 2, monster["damage"] + 2)
        player["hp"] -= dmg
        log.append(f"{monster['name']} ударил вас на {dmg} урона.")

    if player["hp"] <= 0:
        log.append("Вы потеряли сознание... Вас перенесли в безопасное место.")
        player["x"], player["y"] = 2, 2
        player["hp"] = 100

    game_state["log"] = log + game_state["log"]
    return "\n".join(log)

def level_check():
    player = game_state["player"]
    required_exp = player["level"] * 20
    if player["exp"] >= required_exp:
        player["level"] += 1
        player["exp"] = 0
        player["hp"] = 100
        game_state["log"].insert(0, f"Вы достигли уровня {player['level']}! Здоровье восстановлено.")
