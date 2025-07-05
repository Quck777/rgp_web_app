from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Храним игроков по Telegram ID (пока в памяти)
players = {}

locations = ["🏞️ Лес", "⛏️ Шахта", "🏰 Город", "⛰️ Горы"]
monsters = ["🐺 Волк", "🕷️ Паук", "🧟 Зомби", "🐍 Змея"]

def get_player(user_id: str):
    if user_id not in players:
        players[user_id] = {
            "name": f"Игрок {user_id[-4:]}",
            "level": 1,
            "exp": 0,
            "hp": 100,
            "location": "🏰 Город",
            "log": ["🌟 Добро пожаловать в игру!"],
        }
    return players[user_id]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, user_id: str = "anon"):
    player = get_player(user_id)
    return templates.TemplateResponse("index.html", {"request": request, "player": player, "locations": locations})

@app.post("/move")
async def move(request: Request):
    form = await request.form()
    user_id = form.get("user_id")
    location = form.get("location")
    player = get_player(user_id)
    player["location"] = location
    player["log"].append(f"🚶 Переместился в {location}")
    return {"success": True}

@app.post("/fight")
async def fight(request: Request):
    form = await request.form()
    user_id = form.get("user_id")
    player = get_player(user_id)

    monster = random.choice(monsters)
    dmg = random.randint(5, 20)
    player["hp"] -= dmg
    exp = random.randint(10, 25)
    player["exp"] += exp
    player["log"].append(f"⚔️ Битва с {monster} — получил {dmg} урона и {exp} опыта")

    if player["hp"] <= 0:
        player["log"].append("💀 Вы погибли! Возрождение в городе...")
        player["hp"] = 100
        player["location"] = "🏰 Город"

    if player["exp"] >= player["level"] * 100:
        player["level"] += 1
        player["exp"] = 0
        player["log"].append(f"🎉 Новый уровень! Теперь ты {player['level']} ур.")

    return {"success": True}
