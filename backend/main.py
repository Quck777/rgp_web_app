from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="backend/static"), name="static")
templates = Jinja2Templates(directory="backend/templates")

# Игровые данные
player = {
    "name": "Герой",
    "location": "Город",
    "log": [],
    "strength": 1,
    "agility": 1,
    "endurance": 1,
    "points": 5,
    "hp": 10,
}

locations = {
    "Город": "Добро пожаловать в город.",
    "Лес": "Ты вошёл в тёмный лес.",
    "Шахта": "Ты спустился в старую шахту.",
}

monsters = {
    "Лес": {"name": "Волк", "hp": 5, "damage": 2},
    "Шахта": {"name": "Гоблин", "hp": 7, "damage": 3},
    "Город": None,
}


def add_log(message: str):
    player["log"].insert(0, message)
    player["log"] = player["log"][:10]


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "player": player,
        "location": player["location"],
        "description": locations[player["location"]],
    })


@app.post("/move")
async def move(request: Request, place: str = Form(...)):
    player["location"] = place
    add_log(f"🔄 Перемещение: {place}")
    return RedirectResponse("/", status_code=302)


@app.post("/fight")
async def fight(request: Request):
    location = player["location"]
    monster = monsters.get(location)

    if not monster:
        add_log("😐 Здесь нет с кем сражаться.")
        return RedirectResponse("/", status_code=302)

    player_hp = 5 + player["endurance"] * 2
    monster_hp = monster["hp"]
    player_damage = 1 + player["strength"]
    monster_damage = monster["damage"]

    while player_hp > 0 and monster_hp > 0:
        if random.random() < (0.1 + player["agility"] * 0.05):
            add_log("🌀 Ты уклонился от удара!")
        else:
            player_hp -= monster_damage

        monster_hp -= player_damage

    if player_hp > 0:
        add_log(f"🏆 Ты победил {monster['name']}!")
        player["points"] += 1
    else:
        add_log("💀 Ты проиграл...")

    return RedirectResponse("/", status_code=302)


@app.post("/upgrade")
async def upgrade(request: Request, stat: str = Form(...)):
    if player["points"] > 0 and stat in ["strength", "endurance", "agility"]:
        player[stat] += 1
        player["points"] -= 1
        add_log(f"⬆️ Прокачан параметр: {stat.capitalize()} +1")
    return RedirectResponse("/", status_code=302)
