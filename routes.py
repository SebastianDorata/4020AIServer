from flask import Blueprint, render_template
from forms import DietForm
from models import Food, FoodAlias
from db import db

from core.data_classes import MacroTarget
from services.meal_plan_service import MealPlanService
from providers.sample_provider import SampleMealPlanProvider

# Temp imports for sample data
import json
import os

# Flask Blueprint for main.py to register
route_controller = Blueprint(
    "route_controller",
    __name__,
    template_folder="templates"
)


# Calculate Total Daily Energy Expenditure (TDEE)
def calculate_tdee(age, gender, height, weight, activity):

    if gender == "male":
        bmr = (10 * weight + 6.25 * height - 5 * age + 5)

    else:
        bmr = (10 * weight + 6.25 * height - 5 * age - 161)

    tdee = bmr * float(activity)

    return round(tdee, 2)

# Uses tdee and user's goal to determine the target calories
def calculate_target_calories(tdee, goal):
    # 500 cal deficit
    # -1 lb per week
    if goal == "lose":
        return round(tdee - 500, 2)

    # 500 cal increase from tdee
    # +1 lb per week
    elif goal == "gain":
        return round(tdee + 500, 2)
    else:
        # maintain weight
        # Tdee
        return round(tdee, 2)


# Get ideal macronutrient targets used to prompt AI to get meal plan for goal
def calculate_macros(weight, target_calories, goal):
    # Get protein target
    if goal == "lose":
        protein = weight * 2.0
    elif goal == "gain":
        protein = weight * 1.8
    else:
        protein = weight * 1.8

    # Get fat target
    fat_calories = target_calories * 0.25
    fat = fat_calories/9

    # Remaining goes to carbs
    protein_calories = protein * 4
    carb_calories = target_calories - protein_calories - fat_calories

    carbs = carb_calories / 4

    return {
        "protein": round(protein, 2),
        "carbs": round(carbs, 2),
        "fat": round(fat, 2)
    }

# Create full profile for AI
def create_nutrition_profile(age, gender, height, weight, activity, goal):

    tdee = calculate_tdee(
        age,
        gender,
        height,
        weight,
        activity
    )

    target_calories = calculate_target_calories(
        tdee,
        goal
    )

    macros = calculate_macros(
        weight,
        target_calories,
        goal
    )

    goal_display = {
        "lose": "Lose Weight",
        "gain": "Gain Weight",
        "maintain": "Maintain Weight"
    }

    activity_display = {
        "1.2": "Sedentary",
        "1.375": "Light Exercise",
        "1.55": "Moderate Exercise",
        "1.725": "Heavy Exercise",
        "1.9": "Athlete"
    }

    return {

        # User information
        "age": age,
        "gender": gender,
        "height_cm": round(height, 2),
        "height_inches": round(height / 2.54, 2),
        "weight_kg": round(weight, 2),
        "weight_lbs": round(weight * 2.20462, 2),

        # Preferences
        "activity": activity_display[str(activity)],
        "goal": goal_display[goal],

        # Nutrition targets
        "tdee": tdee,
        "target_calories": target_calories,

        "protein": macros["protein"],
        "carbs": macros["carbs"],
        "fat": macros["fat"]
    }


# Home page
# Collects user information and generates nutrition information
@route_controller.route("/", methods=["GET", "POST"])
def home():

    form = DietForm()

    # Runs if code if user submits form
    if form.validate_on_submit():

        # Weight conversion
        height_cm = int(form.height.data) * 2.54
        weight_kg = form.weight.data * 0.453592


        nutrition_profile = create_nutrition_profile(
            form.age.data,
            form.gender.data,
            height_cm,
            weight_kg,
            form.activity.data,
            form.goal.data
        )

        # AI feature: swapping providers (Sample -> Groq -> Ollama) only
        # ever changes this one line, nothing else in this route changes.
        target = MacroTarget(
            calories=nutrition_profile["target_calories"],
            protein_g=nutrition_profile["protein"],
            carbs_g=nutrition_profile["carbs"],
            fat_g=nutrition_profile["fat"],
        )

        meal_plan_service = MealPlanService(SampleMealPlanProvider())
        meal_plan = meal_plan_service.build_plan(target, available_foods=[])

        # Added just to maintain feet / inches separation.
        height_display = dict(form.height.choices).get(form.height.data)

        return render_template(
            "result.html",
            profile=nutrition_profile,
            height_display=height_display,
            meal_plan=meal_plan

        )

    return render_template(
        "index.html",
        form=form
    )

# About page
# Shows group members of assignment
@route_controller.route("/about", methods=["GET"])
def about():
    return render_template("about.html")
