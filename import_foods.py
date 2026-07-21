# ONLY ONE RUN NEEDED, IF NUTRITION.DB IS PRESENT DATA IS ALREADY THERE
# ****************************************** ALREADY RAN DON'T RUN AGAIN ******************************************

import pandas as pd

from main import app
from db import db
from models import Food, FoodAlias


file = "dataset/MyFoodData-Nutrition-Facts-SpreadSheet-Release-1-4.csv"

with app.app_context():

    df = pd.read_csv(file, skiprows=3)

    for _, row in df.iterrows():

        food = Food(
            food_name=row["name"],
            calories=float(row["Calories"]),
            fat=float(row["Fat (g)"]),
            carbs=float(row["Carbohydrate (g)"]),
            protein=float(row["Protein (g)"])
        )

        db.session.add(food)

    db.session.commit()


print("Added .csv data to sqlite database")