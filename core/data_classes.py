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
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float


@dataclass
class Meal:
    meal_name: str
    items: List[MealPlanItem]
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float


@dataclass
class MealPlanResult:
    meals: List[Meal]
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
