from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from backend.game_logic import handle_action, get_location_by_name, DEFAULT_USER

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def root(request: Request):
    user = request.session.get("user", DEFAULT_USER.copy())
    request.session["user"] = user
    location = get_location_by_name(user["location"])
    character = {
        "hp": user["hp"],
        "max_hp": user["max_hp"],
        "attack": user["attack"],
        "defense": user["defense"],
        "level": user["level"]
    }
    return templates.TemplateResponse("index.html", {
        "request": request,
        "location": location["name"],
        "character": character,
        "log": user.get("log", []),
        "inventory": user.get("inventory", {}),
        "gold": user.get("gold", 0)
    })

@app.post("/action")
async def do_action(request: Request, action: str = Form(...)):
    user = request.session.get("user", DEFAULT_USER.copy())
    log_entry = handle_action(user, action)
    user.setdefault("log", []).insert(0, log_entry)
    request.session["user"] = user
    return RedirectResponse("/", status_code=303)
