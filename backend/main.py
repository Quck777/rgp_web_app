from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="backend/static"), name="static")
templates = Jinja2Templates(directory="backend/templates")

# Игровое состояние
player = {
    "hp": 100,
    "attack": 10,
    "xp": 0,
    "level": 1,
    "location": "Город",
    "log": []
}

monsters = [
    {"name": "Волк", "hp": 30, "attack": 5},
    {"name": "Гоблин", "hp": 40, "attack": 6},
    {"name": "Паук", "hp": 25, "attack": 4},
]

current_monster = None


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "player": player,
        "monster": current_monster
    })


@app.post("/move")
def move(location: str = Form(...)):
    player["location"] = location
    player["log"].append(f"🔸 Переместился в {location}")
    global current_monster
    current_monster = None

    if location == "Лес":
        current_monster = random.choice(monsters).copy()
        player["log"].append(f"⚔️ В лесу появился монстр: {current_monster['name']}")

    return RedirectResponse("/", status_code=303)


@app.post("/attack")
def attack():
    global current_monster
    if not current_monster:
        return RedirectResponse("/", status_code=303)

    dmg_to_monster = player["attack"]
    current_monster["hp"] -= dmg_to_monster
    player["log"].append(f"🗡 Ты ударил {current_monster['name']} на {dmg_to_monster} HP")

    if current_monster["hp"] <= 0:
        player["log"].append(f"✅ Ты победил {current_monster['name']}!")
        player["xp"] += 25
        if player["xp"] >= 100:
            player["xp"] -= 100
            player["level"] += 1
            player["attack"] += 2
            player["hp"] = 100
            player["log"].append(f"🌟 Новый уровень! Ты теперь {player['level']} уровня!")
        current_monster = None
    else:
        dmg_to_player = current_monster["attack"]
        player["hp"] -= dmg_to_player
        player["log"].append(f"💥 {current_monster['name']} ударил тебя на {dmg_to_player} HP")

    if player["hp"] <= 0:
        player["log"].append("💀 Ты погиб... Игра начинается заново.")
        player["hp"] = 100
        player["xp"] = 0
        player["level"] = 1
        player["attack"] = 10
        current_monster = None

    return RedirectResponse("/", status_code=303)
