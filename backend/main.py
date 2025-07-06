# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from story_engine import StoryEngine

app = FastAPI()
engine = StoryEngine()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    text: str

@app.post("/action")
def play_turn(input: UserInput):
    return engine.process_action(input.text)
