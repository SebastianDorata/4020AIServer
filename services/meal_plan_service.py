from typing import List

from core.data_classes import MacroTarget, FoodItem, MealPlanResult
from providers.provider import MealPlanProvidable


class MealPlanService:
    def __init__(self, provider: MealPlanProvidable):
        self.provider = provider

    def build_plan(
        self, target: MacroTarget, available_foods: List[FoodItem]
    ) -> MealPlanResult:
        return self.provider.generate_meal_plan(target, available_foods)
