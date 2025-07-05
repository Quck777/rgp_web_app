from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.game_logic import game_state, move_player

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")
templates = Jinja2Templates(directory="frontend")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "player": game_state["player"],
        "log": game_state["log"],
        "map": game_state["map"]
    })

@app.post("/move/{direction}")
async def move(direction: str):
    result = move_player(direction)
    return {"status": "ok", "result": result, "player": game_state["player"], "log": game_state["log"]}
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "player": game_state["player"],
        "log": game_state["log"],
        "map": game_state["map"],
        "monsters": game_state["monsters"]
    })
