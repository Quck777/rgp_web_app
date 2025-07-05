from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

current_location = {"name": "Город"}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "location": current_location["name"]
    })

@app.post("/move", response_class=RedirectResponse)
async def move(location: str = Form(...)):
    current_location["name"] = location
    return RedirectResponse(url="/", status_code=303)
