import json
from typing import List, Optional

from core.data_classes import MacroTarget, FoodItem, MealPlanResult, MealPlanItem, Meal
from db import db
from models import Food, FoodAlias


class SampleMealPlanProvider:
    """What the repo currently uses (hardcoded sample plans). Reads a canned
    JSON meal plan and resolves each food name against the database using the
    same alias-then-exact-match lookup that used to live in routes.py.

    Note: `available_foods` is part of the interface (real AI providers need
    it to know what's in the catalog) but this provider ignores it — it
    already looks foods up directly via the alias table, since the sample
    plan is fixed rather than generated from the catalog.
    """

    def __init__(self, sample_file: str = "sample_data/sample_meal_gpt_mini.json"):
        self.sample_file = sample_file

    def generate_meal_plan(
        self, target: MacroTarget, available_foods: List[FoodItem]
    ) -> MealPlanResult:
        with open(self.sample_file, "r") as f:
            sample = json.load(f)

        meals: List[Meal] = []
        total_calories = total_protein = total_carbs = total_fat = 0.0

        for meal_data in sample["meal_plan"]:
            items: List[MealPlanItem] = []
            meal_calories = meal_protein = meal_carbs = meal_fat = 0.0

            for entry in meal_data["foods"]:
                food = self._resolve_food(entry["food"])
                if not food:
                    continue  # same "skip if not found" behaviour as before

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
    def _resolve_food(food_name: str) -> Optional[Food]:
        """Same two-step lookup as the old get_food_info(): curated alias
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
