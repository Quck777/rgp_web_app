# backend/story_engine.py
import random

class StoryEngine:
    def __init__(self):
        self.state = {
            "location": "деревня Ардхольм",
            "chapter": 1,
            "history": []
        }

    def roll_dice(self):
        return random.randint(1, 12)

    def process_action(self, user_input: str):
        roll = self.roll_dice()
        result = ""

        if roll <= 4:
            outcome = "неудача"
            result = "Вы спотыкаетесь и теряете возможность действовать."
        elif 5 <= roll <= 8:
            outcome = "нейтрально"
            result = "Вы едва справляетесь, но не достигаете многого."
        else:
            outcome = "успех"
            result = "Ваше действие приносит плоды!"

        response = {
            "chapter": self.state["chapter"],
            "location": self.state["location"],
            "action": user_input,
            "dice_roll": roll,
            "outcome": outcome,
            "result": result,
        }

        self.state["history"].append(response)
        self.state["chapter"] += 1
        return response
