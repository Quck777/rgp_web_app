from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from backend.game_logic import (
    init_user, get_current_location, add_log,
    gather_resources, get_inventory_by_category,
    remove_item, sell_item
)

app = FastAPI()

# Подключение статики и шаблонов
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Секретный ключ для сессий
app.add_middleware(SessionMiddleware, secret_key="secret-key")

# Корневая страница
@app.get("/")
def root(request: Request):
    if "user" not in request.session:
        request.session["user"] = init_user()

    current_location = get_current_location(request)
    inventory = get_inventory_by_category(request)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "location": current_location["name"],
        "actions": current_location["actions"],
        "stats": request.session["user"]["stats"],
        "inventory": inventory,
        "log": request.session["user"]["log"],
        "gold": request.session["user"].get("gold", 0)
    })

# Обработка действий: перемещение, прокачка и сбор
@app.post("/action")
def handle_action(request: Request, action: str = Form(...)):
    user = request.session.get("user")

    if action in ["forest", "mine", "town"]:
        user["location"] = action
        add_log(request, f"Вы переместились в локацию: {action}")
    elif action.startswith("upgrade_"):
        stat = action.replace("upgrade_", "")
        if stat in user["stats"]:
            user["stats"][stat] += 1
            add_log(request, f"Вы улучшили характеристику: {stat}")
    elif action == "gather":
        location = user["location"]
        gather_resources(location, request)

    request.session.modified = True
    return RedirectResponse("/", status_code=303)

# Удаление предмета
@app.post("/remove")
def handle_remove(request: Request, item: str = Form(...)):
    remove_item(request, item)
    add_log(request, f"Вы удалили предмет: {item}")
    return RedirectResponse("/", status_code=303)

# Продажа предмета
@app.post("/sell")
def handle_sell(request: Request, item: str = Form(...)):
    sell_item(request, item)
    return RedirectResponse("/", status_code=303)
