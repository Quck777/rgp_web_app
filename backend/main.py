from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="backend/static"), name="static")
templates = Jinja2Templates(directory="backend/templates")

# Игрок и игра
current_location = {"name": "Город"}
event_log = []
player_hp = 100
monster = None

monsters = [
    {"name": "Гоблин", "hp": 30, "damage": 10},
    {"name": "Орк", "hp": 50, "damage": 15},
    {"name": "Слизень", "hp": 20, "damage": 5}
]

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "location": current_location["name"],
        "log": event_log[-5:][::-1],  # последние 5 сообщений
        "show_attack": current_location["name"] == "Лес" and monster is not None,
        "monster": monster,
        "player_hp": player_hp
    })

@app.post("/move")
async def move(request: Request, destination: str = Form(...)):
    global monster
    current_location["name"] = destination
    event_log.append(f"Ты переместился в {destination}.")
    if destination == "Лес":
        monster = random.choice(monsters).copy()
        event_log.append(f"В лесу появился монстр: {monster['name']} с {monster['hp']} HP.")
    else:
        monster = None
    return RedirectResponse("/", status_code=302)

@app.post("/attack")
async def attack(request: Request):
    global monster, player_hp
    if monster:
        damage = random.randint(8, 15)
        monster["hp"] -= damage
        event_log.append(f"Ты ударил монстра на {damage} урона.")
        if monster["hp"] <= 0:
            event_log.append(f"Ты победил монстра {monster['name']}!")
            monster = None
        else:
            retaliation = monster["damage"]
            player_hp -= retaliation
            event_log.append(f"{monster['name']} атакует тебя на {retaliation} урона!")
    return RedirectResponse("/", status_code=302)
