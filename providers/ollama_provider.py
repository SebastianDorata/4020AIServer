from typing import List

from core.data_classes import MacroTarget, FoodItem, MealPlanResult


class OllamaMealPlanProvider:
    def generate_meal_plan(
        self, target: MacroTarget, available_foods: List[FoodItem]
    ) -> MealPlanResult:
        raise NotImplementedError("TODO: call local Ollama /api/chat, "
                                   "parse structured JSON response into MealPlanResult")
