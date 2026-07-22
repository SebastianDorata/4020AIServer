from typing import List

from core.data_classes import MacroTarget, FoodItem, MealPlanResult


class GroqMealPlanProvider:
    def generate_meal_plan(
        self, target: MacroTarget, available_foods: List[FoodItem]
    ) -> MealPlanResult:
        raise NotImplementedError("TODO: prompt Groq with target + available_foods, "
                                   "parse structured JSON response into MealPlanResult")
