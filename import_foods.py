# ONLY ONE RUN NEEDED, IF NUTRITION.DB IS PRESENT DATA IS ALREADY THERE
# ****************************************** ALREADY RAN DON'T RUN AGAIN ******************************************

import pandas as pd

from main import app
from db import db
from models import Food


files = [
    "dataset/FOOD-DATA-GROUP1.csv",
    "dataset/FOOD-DATA-GROUP2.csv",
    "dataset/FOOD-DATA-GROUP3.csv",
    "dataset/FOOD-DATA-GROUP4.csv",
    "dataset/FOOD-DATA-GROUP5.csv"
]


# Read all .csv files and import the data into sqlite database
with app.app_context():

    for file in files:

        df = pd.read_csv(file)

        for _, row in df.iterrows():

            food = Food(
                food_name=row["food"],
                calories=row["Caloric Value"],
                fat=row["Fat"],
                carbs=row["Carbohydrates"],
                protein=row["Protein"],
                fiber=row["Dietary Fiber"]
            )

            db.session.add(food)

    db.session.commit()


print("Added .csv data to sqlite database")