import json
import os
from typing import List, Optional

import requests

from core.data_classes import MacroTarget, FoodItem, MealPlanResult, MealPlanItem, Meal
from db import db
from models import Food, FoodAlias


class OllamaMealPlanProvider:
    """Implements MealPlanProvidable via a local/containerized Ollama model.
    No API key, no internet dependency once the model is pulled — good for
    a live demo since it can't rate-limit or go down mid-presentation.
    """

    def __init__(self, model: str = "llama3.2"):
        self.model = model
        # Reads OLLAMA_HOST from the environment so this works both:
        # - inside Docker Compose (OLLAMA_HOST=http://ollama:11434)
        # - running locally/PyCharm without Docker (falls back to localhost,
        #   which still reaches the container via the exposed port mapping)
        self.host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

    def generate_meal_plan(
            self, target: MacroTarget, available_foods: List[FoodItem]
    ) -> MealPlanResult:
        prompt = self._build_prompt(target, available_foods)

        response = requests.post(
            f"{self.host}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "format": "json",
                "stream": False,
                # Keeps the model resident in memory between requests so we
                # don't pay the ~4s load cost again on the next request.
                "keep_alive": "30m",
                "options": {
                    # Hard cap on generated tokens. Real output has been
                    # ~200 tokens for a full 3-meal plan; 400 gives headroom
                    # without letting a run-on generation blow up demo time.
                    "num_predict": 400,
                    # Prompt + response comfortably fit well under the
                    # default 2048-token context; shrinking it reduces
                    # per-request allocation overhead.
                    "num_ctx": 1024,
                },
            },
            timeout=60,
        )
        response.raise_for_status()

        raw = json.loads(response.json()["response"])
        return self.build_meal_plan_result(raw)

    @staticmethod
    def _build_prompt(target: MacroTarget, available_foods: List[FoodItem]) -> str:
        food_names = ", ".join(f.name for f in available_foods) if available_foods else "any common foods"
        return f"""You are a nutrition planning assistant. Create a one-day meal plan
that totals approximately {target.calories} calories, {target.protein_g}g protein,
{target.carbs_g}g carbs, and {target.fat_g}g fat.

Choose from foods like: {food_names}

Include exactly 3 meals: Breakfast, Lunch, and Dinner.
Each meal must have 2 to 3 foods only. Do not add snacks or extra meals.

Respond with ONLY valid JSON in this exact shape, no other text:
{{
  "meal_plan": [
    {{
      "meal_name": "Breakfast",
      "foods": [
        {{"food": "chicken breast", "grams": 150}}
      ]
    }}
  ]
}}"""



    def build_meal_plan_result(self, raw: dict) -> MealPlanResult:
        """Same resolution + totalling logic as SampleMealPlanProvider: look each
        AI-suggested food up via the alias table, then exact-match fallback, and
        compute real calories/macros from the per-100g values in the database."""
        meals: List[Meal] = []
        total_calories = total_protein = total_carbs = total_fat = 0.0

        for meal_data in raw["meal_plan"]:
            items: List[MealPlanItem] = []
            meal_calories = meal_protein = meal_carbs = meal_fat = 0.0

            for entry in meal_data["foods"]:
                food = self.resolve_food(entry["food"])

                if not food:
                    continue  # AI suggested something not in the catalog — skip it

                multiplier = entry["grams"] / 100
                calories = round(food.calories * multiplier, 2)
                protein = round(food.protein * multiplier, 2)
                carbs = round(food.carbs * multiplier, 2)
                fat = round(food.fat * multiplier, 2)

                items.append(MealPlanItem(
                    food_name=entry["food"].title(),
                    portion_grams=entry["grams"],
                    calories=calories,
                    protein_g=protein,
                    carbs_g=carbs,
                    fat_g=fat,
                ))

                meal_calories += calories
                meal_protein += protein
                meal_carbs += carbs
                meal_fat += fat

            meals.append(Meal(
                meal_name=meal_data["meal_name"],
                items=items,
                total_calories=round(meal_calories, 2),
                total_protein_g=round(meal_protein, 2),
                total_carbs_g=round(meal_carbs, 2),
                total_fat_g=round(meal_fat, 2),
            ))

            total_calories += meal_calories
            total_protein += meal_protein
            total_carbs += meal_carbs
            total_fat += meal_fat

        return MealPlanResult(
            meals=meals,
            total_calories=round(total_calories, 2),
            total_protein_g=round(total_protein, 2),
            total_carbs_g=round(total_carbs, 2),
            total_fat_g=round(total_fat, 2),
        )

    @staticmethod
    def resolve_food(food_name: str) -> Optional[Food]:
        """Same two-step lookup as SampleMealPlanProvider: curated alias
        first, then exact name match as a fallback."""
        normalized = food_name.strip().lower()

        alias = db.session.execute(
            db.select(FoodAlias).where(
                db.func.lower(FoodAlias.search_term) == normalized
            )
        ).scalar_one_or_none()

        if alias:
            return db.session.get(Food, alias.food_id)

        return db.session.execute(
            db.select(Food).where(
                db.func.lower(Food.food_name) == normalized
            )
        ).scalar_one_or_none()