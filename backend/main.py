from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="backend/static"), name="static")
templates = Jinja2Templates(directory="backend/templates")

# Стартовая локация
current_location = {"name": "Город"}

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "location": current_location["name"]
    })

@app.post("/move")
async def move(request: Request, destination: str = Form(...)):
    current_location["name"] = destination
    return RedirectResponse("/", status_code=302)
