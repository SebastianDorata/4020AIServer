from dataclasses import dataclass
from typing import List


@dataclass
class MacroTarget:
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float


@dataclass
class FoodItem:
    name: str
    calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fat_per_100g: float


@dataclass
class MealPlanItem:
    food_name: str
    portion_grams: float


@dataclass
class MealPlanResult:
    items: List[MealPlanItem]
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float


@dataclass
class EvaluationResult:
    calorie_diff_pct: float
    protein_diff_pct: float
    carbs_diff_pct: float
    fat_diff_pct: float


def evaluate_plan(target: MacroTarget, plan: MealPlanResult) -> EvaluationResult:
    def pct_diff(actual: float, goal: float) -> float:
        return round(((actual - goal) / goal) * 100, 1) if goal else 0.0

    return EvaluationResult(
        calorie_diff_pct=pct_diff(plan.total_calories, target.calories),
        protein_diff_pct=pct_diff(plan.total_protein_g, target.protein_g),
        carbs_diff_pct=pct_diff(plan.total_carbs_g, target.carbs_g),
        fat_diff_pct=pct_diff(plan.total_fat_g, target.fat_g),
    )