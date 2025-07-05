from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="backend/static"), name="static")
templates = Jinja2Templates(directory="backend/templates")

# 🔹 Персонаж
player = {
    "name": "Герой",
    "level": 1,
    "exp": 0,
    "gold": 0,
    "hp": 100,
    "attack": 10,
    "inventory": [],
}

# 🔹 Локации
locations = {
    "forest": {"name": "Лес", "reward": {"exp": 10, "gold": 5}},
    "mine": {"name": "Шахта", "reward": {"exp": 5, "gold": 15}},
    "city": {"name": "Город", "reward": {"exp": 0, "gold": 0}},
}
current_location = {"key": "city", "name": locations["city"]["name"]}

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "location": current_location["name"],
        "player": player
    })

@app.post("/move")
async def move_location(request: Request, place: str = Form(...)):
    if place in locations:
        current_location["key"] = place
        current_location["name"] = locations[place]["name"]

        reward = locations[place]["reward"]
        player["exp"] += reward["exp"]
        player["gold"] += reward["gold"]

        # Уровень = 1 + (опыт // 100)
        player["level"] = 1 + player["exp"] // 100

    return RedirectResponse(url="/", status_code=302)
