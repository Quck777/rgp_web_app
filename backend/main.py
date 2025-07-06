from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="backend/static"), name="static")
templates = Jinja2Templates(directory="backend/templates")

# Игровое состояние
state = {
    "location": "Лес",
    "logs": ["Добро пожаловать в игру!"],
    "enemy": None,
    "player": {
        "hp": 100,
        "attack": 10,
        "level": 1,
        "exp": 0
    }
}

enemies_by_location = {
    "Лес": [{"name": "Волк", "hp": 30, "attack": 5}, {"name": "Медведь", "hp": 50, "attack": 8}],
    "Шахта": [{"name": "Гоблин", "hp": 40, "attack": 6}, {"name": "Голем", "hp": 70, "attack": 10}],
    "Город": [{"name": "Разбойник", "hp": 35, "attack": 7}, {"name": "Преступник", "hp": 45, "attack": 9}]
}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "location": state["location"],
        "logs": state["logs"],
        "enemy": state["enemy"],
        "player": state["player"]
    })

@app.post("/move")
async def move(location: str = Form(...)):
    state["location"] = location
    state["logs"].append(f"Вы перешли в локацию: {location}")
    return RedirectResponse("/", status_code=302)

@app.post("/explore")
async def explore():
    location = state["location"]
    enemy = random.choice(enemies_by_location[location])
    state["enemy"] = enemy.copy()
    state["logs"].append(f"Вы встретили врага: {enemy['name']}!")
    return RedirectResponse("/", status_code=302)

@app.post("/fight")
async def fight():
    player = state["player"]
    enemy = state["enemy"]

    if not enemy:
        state["logs"].append("Нет врага для атаки.")
        return RedirectResponse("/", status_code=302)

    player_damage = random.randint(player["attack"] - 3, player["attack"] + 3)
    enemy["hp"] -= player_damage
    state["logs"].append(f"Вы нанесли {player_damage} урона врагу ({enemy['name']})")

    if enemy["hp"] <= 0:
        exp_gain = 10
        player["exp"] += exp_gain
        state["logs"].append(f"Вы победили врага {enemy['name']} и получили {exp_gain} опыта!")
        state["enemy"] = None
    else:
        enemy_damage = random.randint(enemy["attack"] - 2, enemy["attack"] + 2)
        player["hp"] -= enemy_damage
        state["logs"].append(f"Враг {enemy['name']} атаковал вас и нанёс {enemy_damage} урона!")

    return RedirectResponse("/", status_code=302)
