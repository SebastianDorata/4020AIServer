from typing import Protocol, List

from dataClasses import MacroTarget, FoodItem, MealPlanResult


class MealPlanProvidable(Protocol):
    def generate_meal_plan(
        self, target: MacroTarget, available_foods: List[FoodItem]
    ) -> MealPlanResult:
        ...