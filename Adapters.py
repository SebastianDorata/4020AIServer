from typing import List

from dataClasses import MacroTarget, FoodItem, MealPlanResult


class GroqMealPlanProvider:
    def generate_meal_plan(
        self, target: MacroTarget, available_foods: List[FoodItem]
    ) -> MealPlanResult:
        raise NotImplementedError("TODO: prompt Groq with target + available_foods, "
                                   "parse structured JSON response into MealPlanResult")


class OllamaMealPlanProvider:
    def generate_meal_plan(
        self, target: MacroTarget, available_foods: List[FoodItem]
    ) -> MealPlanResult:
        raise NotImplementedError("TODO: call local Ollama /api/chat, "
                                   "parse structured JSON response into MealPlanResult")


class SampleMealPlanProvider:
    """What the repo currently uses (hardcoded sample plans). Keeping this as a
    real implementation of the interface means routes.py already works today,
    and swapping in the real AI later is a one-line change in the composition root."""

    def generate_meal_plan(
        self, target: MacroTarget, available_foods: List[FoodItem]
    ) -> MealPlanResult:
        # existing sample-plan logic goes here, unchanged from current behaviour
        raise NotImplementedError("TODO: move existing sample plan logic here")