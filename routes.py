from flask import Blueprint, render_template
from forms import DietForm
from models import Food
from db import db

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


# Queries database for food nutrition information
def get_food_info(food_name):

    normalized = food_name.strip().lower()

    # 1. Exact case-insensitive match
    food = db.session.execute(
        db.select(Food)
        .where(db.func.lower(Food.food_name) == normalized)
    ).scalars().first()

    if food:
        return food

    # 2. Starts-with match
    food = db.session.execute(
        db.select(Food)
        .where(db.func.lower(Food.food_name).like(f"{normalized}%"))
    ).scalars().first()

    if food:
        return food

    # 3. Contains match as fallback
    food = db.session.execute(
        db.select(Food)
        .where(db.func.lower(Food.food_name).like(f"%{normalized}%"))
    ).scalars().first()

    return food

# Calculates nutrition values based on specified grams
# Nutrition values in database are per 100 grams
def calculate_food_nutrition(food_name, grams):

    food = get_food_info(food_name)

    if not food:
        return None

    # Example:
    # 50 grams = 0.5 multiplier
    multiplier = grams / 100

    return {
        "food": food.food_name,
        "grams": grams,
        "calories": round(food.calories * multiplier, 2),
        "protein": round(food.protein * multiplier, 2),
        "carbs": round(food.carbs * multiplier, 2),
        "fat": round(food.fat * multiplier, 2)
    }


# Calculates nutrition information for a meal containing multiple foods
def calculate_meal_nutrition(meal):

    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0

    food_results = []

    for food in meal:

        nutrition = calculate_food_nutrition(
            food["food"],
            food["grams"]
        )

        if nutrition:

            food_results.append(nutrition)

            total_calories += nutrition["calories"]
            total_protein += nutrition["protein"]
            total_carbs += nutrition["carbs"]
            total_fat += nutrition["fat"]

    return {
        "foods": food_results,
        "total_calories": round(total_calories, 2),
        "total_protein": round(total_protein, 2),
        "total_carbs": round(total_carbs, 2),
        "total_fat": round(total_fat, 2)
    }

# Wrapper funciton to get daily meals total
def calculate_daily_meal_nutrition(meal_plan):

    daily_totals = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0
    }

    meals = []

    for meal in meal_plan["meal_plan"]:

        nutrition = calculate_meal_nutrition(
            meal["foods"]
        )

        meals.append(
            {
                "meal_name": meal["meal_name"],
                "nutrition": nutrition
            }
        )

        daily_totals["calories"] += nutrition["total_calories"]
        daily_totals["protein"] += nutrition["total_protein"]
        daily_totals["carbs"] += nutrition["total_carbs"]
        daily_totals["fat"] += nutrition["total_fat"]


    return {
        "meals": meals,
        "daily_totals": {
            "calories": round(daily_totals["calories"],2),
            "protein": round(daily_totals["protein"],2),
            "carbs": round(daily_totals["carbs"],2),
            "fat": round(daily_totals["fat"],2)
        }
    }



# loader func for sample meal and eventually ai-response
def load_sample_meal(filename):
    with open(filename, "r") as file:
        return json.load(file)




# Home page
# Collects user information and generates nutrition information
@route_controller.route("/", methods=["GET", "POST"])
def home():

    form = DietForm()
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


        sample_meal = load_sample_meal("sample_data/sample_meal_gpt_mini.json")



        meal_plan = calculate_daily_meal_nutrition(
            sample_meal
        )

        print(nutrition_profile)
        print(meal_plan)

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
