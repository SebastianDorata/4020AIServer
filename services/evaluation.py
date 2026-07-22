from core.data_classes import MacroTarget, MealPlanResult, EvaluationResult


def evaluate_plan(target: MacroTarget, plan: MealPlanResult) -> EvaluationResult:
    def pct_diff(actual: float, goal: float) -> float:
        return round(((actual - goal) / goal) * 100, 1) if goal else 0.0

    return EvaluationResult(
        calorie_diff_pct=pct_diff(plan.total_calories, target.calories),
        protein_diff_pct=pct_diff(plan.total_protein_g, target.protein_g),
        carbs_diff_pct=pct_diff(plan.total_carbs_g, target.carbs_g),
        fat_diff_pct=pct_diff(plan.total_fat_g, target.fat_g),
    )
