# ONLY ONE RUN NEEDED, IF NUTRITION.DB IS PRESENT DATA IS ALREADY THERE
# ****************************************** ALREADY RAN DON'T RUN AGAIN ******************************************

from main import app
from db import db
from models import Food, FoodAlias

# Aliases to correctly match ai picked foods with actual db entities

aliases = [
    {
        "search": "greek yogurt",
        "food": "Nonfat Greek Yogurt"
    },
    {
        "search": "nonfat greek yogurt",
        "food": "Nonfat Greek Yogurt"
    },
    {
        "search": "plain greek yogurt",
        "food": "Greek Yogurt (Plain)"
    },
    {
        "search": "cottage cheese",
        "food": "Cottage Cheese (Blended)"
    },
    {
        "search": "low fat cottage cheese",
        "food": "Lowfat Cottage Cheese (2%)"
    },
    {
        "search": "nonfat cottage cheese",
        "food": "Nonfat Cottage Cheese"
    },
    {
        "search": "chicken breast",
        "food": "Lean Chicken Breast (Cooked)"
    },
    {
        "search": "grilled chicken breast",
        "food": "Lean Chicken Breast (Cooked)"
    },
    {
        "search": "baked chicken breast",
        "food": "Lean Chicken Breast (Cooked)"
    },
    {
        "search": "shredded chicken breast",
        "food": "Lean Chicken Breast (Cooked)"
    },
    {
        "search": "ground chicken",
        "food": "Chicken Ground"
    },
    {
        "search": "lean ground chicken",
        "food": "Chicken Ground"
    },
    {
        "search": "ground turkey",
        "food": "Ground Turkey Cooked"
    },
    {
        "search": "lean ground turkey",
        "food": "Fat Free Ground Turkey"
    },
    {
        "search": "turkey breast",
        "food": "Roasted Turkey Breast"
    },
    {
        "search": "deli turkey",
        "food": "Turkey White Rotisserie Deli Cut"
    },
    {
        "search": "tuna",
        "food": "Canned White Tuna (Water Packed)"
    },
    {
        "search": "canned tuna",
        "food": "Canned White Tuna (Water Packed)"
    },
    {
        "search": "tuna in water",
        "food": "Canned White Tuna (Water Packed)"
    },
    {
        "search": "salmon",
        "food": "Wild Atlantic Salmon (Cooked)"
    },
    {
        "search": "baked salmon",
        "food": "Wild Atlantic Salmon (Cooked)"
    },
    {
        "search": "shrimp",
        "food": "Cooked Shrimp"
    },
    {
        "search": "lean ground beef",
        "food": "Beef Ground 90% Lean Meat / 10% Fat Crumbles Cooked Pan-Browned"
    },
    {
        "search": "ground beef",
        "food": "Ground Beef Cooked"
    },
    {
        "search": "sirloin steak",
        "food": "Beef Top Sirloin Steak Separable Lean And Fat Trimmed To 0 Inch Fat Select Cooked Broiled"
    },
    {
        "search": "top sirloin",
        "food": "Beef Top Sirloin Steak Separable Lean And Fat Trimmed To 0 Inch Fat Select Cooked Broiled"
    },
    {
        "search": "steak",
        "food": "Beef Top Sirloin Steak Separable Lean And Fat Trimmed To 0 Inch Fat Select Cooked Broiled"
    },
    {
        "search": "egg whites",
        "food": "Egg Whites (Raw)"
    },
    {
        "search": "liquid egg whites",
        "food": "Egg Whites (Raw)"
    },
    {
        "search": "scrambled eggs",
        "food": "Scrambled Eggs"
    },
    {
        "search": "whole eggs",
        "food": "Egg Whole Cooked Ns As To Cooking Method"
    },
    {
        "search": "eggs",
        "food": "Egg Whole Cooked Ns As To Cooking Method"
    },
    {
        "search": "protein oats",
        "food": "Oats Regular And Quick Not Fortified Dry"
    },
    {
        "search": "oatmeal",
        "food": "Oats Regular And Quick And Instant Unenriched Cooked With Water (Includes Boiling And Microw"
    },
    {
        "search": "rolled oats",
        "food": "Oats Regular And Quick Not Fortified Dry"
    },
    {
        "search": "overnight oats",
        "food": "Oats Regular And Quick Not Fortified Dry"
    },
    {
        "search": "white rice",
        "food": "White Rice"
    },
    {
        "search": "brown rice",
        "food": "Brown Rice"
    },
    {
        "search": "jasmine rice",
        "food": "Rice White Long-Grain Regular Cooked Unenriched With Salt"
    },
    {
        "search": "basmati rice",
        "food": "Rice White Long-Grain Regular Cooked Unenriched With Salt"
    },
    {
        "search": "sweet potato",
        "food": "Cooked Sweet Potatoes"
    },
    {
        "search": "baked sweet potato",
        "food": "Cooked Sweet Potatoes"
    },
    {
        "search": "potato",
        "food": "Baked Potatoes"
    },
    {
        "search": "baked potato",
        "food": "Baked Potatoes"
    },
    {
        "search": "roasted potato",
        "food": "Baked Potatoes"
    },
    {
        "search": "whole wheat bread",
        "food": "Whole Wheat Bread"
    },
    {
        "search": "toast",
        "food": "Toasted White Bread"
    },
    {
        "search": "pasta",
        "food": "Pasta Cooked"
    },
    {
        "search": "whole wheat pasta",
        "food": "Whole Wheat Pasta"
    },
    {
        "search": "banana",
        "food": "Bananas"
    },
    {
        "search": "apple",
        "food": "Apples"
    },
    {
        "search": "blueberries",
        "food": "Blueberries"
    },
    {
        "search": "strawberries",
        "food": "Strawberries"
    },
    {
        "search": "broccoli",
        "food": "Broccoli (Cooked)"
    },
    {
        "search": "steamed broccoli",
        "food": "Broccoli (Cooked)"
    },
    {
        "search": "spinach",
        "food": "Spinach"
    },
    {
        "search": "raw spinach",
        "food": "Spinach"
    },
    {
        "search": "kale",
        "food": "Kale"
    },
    {
        "search": "romaine lettuce",
        "food": "Romaine Lettuce Raw"
    },
    {
        "search": "iceberg lettuce",
        "food": "Iceberg Lettuce"
    },
    {
        "search": "mixed greens",
        "food": "Vegetables Mixed Frozen Cooked Boiled Drained With Salt"
    },
    {
        "search": "carrots",
        "food": "Carrots"
    },
    {
        "search": "baby carrots",
        "food": "Baby Carrots"
    },
    {
        "search": "zucchini",
        "food": "Zucchini"
    },
    {
        "search": "mushrooms",
        "food": "Mushrooms Cooked From Fresh Ns As To Fat Added In Cooking"
    },
    {
        "search": "onions",
        "food": "Onions"
    },
    {
        "search": "tomato",
        "food": "Tomatoes"
    },
    {
        "search": "peanut butter",
        "food": "Peanut Butter (Smooth)"
    },
    {
        "search": "natural peanut butter",
        "food": "Peanut Butter (Smooth)"
    },
    {
        "search": "rice cakes",
        "food": "Snacks Rice Cakes Brown Rice Plain Unsalted"
    },
    {
        "search": "plain rice cakes",
        "food": "Snacks Rice Cakes Brown Rice Plain Unsalted"
    },
    {
        "search": "avocado",
        "food": "Avocados"
    },
    {
        "search": "black beans",
        "food": "Black Beans"
    },
    {
        "search": "green beans",
        "food": "Cooked Green Beans (Previously Frozen)"
    },
    {
        "search": "asparagus",
        "food": "Asparagus"
    },
    {
        "search": "cauliflower",
        "food": "Cauliflower"
    },
    {
        "search": "plain yogurt",
        "food": "Plain Yogurt"
    },
    {
        "search": "skyr",
        "food": "Nonfat Greek Yogurt"
    },
    {
        "search": "turkey burger patty",
        "food": "Ground Turkey Cooked"
    },
    {
        "search": "chicken thighs",
        "food": "Roasted Chicken Thigh"
    },
    {
        "search": "cod",
        "food": "Cod Baked Or Broiled Made Without Fat"
    },
    {
        "search": "tilapia",
        "food": "Cooked Tilapia"
    },
    {
        "search": "pork tenderloin",
        "food": "Pork Tenderloin Cooked Ns As To Cooking Method"
    },
    {
        "search": "ham",
        "food": "Ham Fresh Cooked Lean Only Eaten"
    },
    {
        "search": "quinoa",
        "food": "Quinoa Cooked"
    },
    {
        "search": "english muffin",
        "food": "English Muffins"
    },
    {
        "search": "bagel",
        "food": "Bagel"
    },
    {
        "search": "wrap",
        "food": "Mission Foods Mission Flour Tortillas Soft Taco 8 Inch"
    },
    {
        "search": "whole wheat tortilla",
        "food": "Tortillas Ready-To-Bake Or -Fry Whole Wheat"
    },
    {
        "search": "granola",
        "food": "Cereal Granola"
    },
    {
        "search": "almonds",
        "food": "Almonds"
    },
    {
        "search": "mixed nuts",
        "food": "Mixed Nuts Nfs"
    },
    {
        "search": "olive oil",
        "food": "Olive Oil"
    },
    {
        "search": "cheddar cheese",
        "food": "Cheddar Cheese"
    },
    {
        "search": "mozzarella cheese",
        "food": "Mozzarella"
    },
    {
        "search": "fairlife milk",
        "food": "Milk Reduced Fat Fluid 2% Milkfat Protein Fortified With Added Vitamin A And Vitamin D"
    },
    {
        "search": "2% milk",
        "food": "Low-Fat Milk 2%"
    },
    {
        "search": "almond milk",
        "food": "Almond Milk Unsweetened"
    },
    {
        "search": "rice",
        "food": "White Rice"
    },
    {
        "search": "chicken",
        "food": "Lean Chicken Breast (Cooked)"
    },
    {
        "search": "beef",
        "food": "Beef Ground Cooked"
    },
    {
        "search": "fish",
        "food": "Cod Baked Or Broiled Made Without Fat"
    },
    {
        "search": "yogurt",
        "food": "Greek Yogurt (Plain)"
    },
    {
        "search": "oats",
        "food": "Oats Regular And Quick Not Fortified Dry"
    },
    {
        "search": "potatoes",
        "food": "Baked Potatoes"
    },
    {
        "search": "berries",
        "food": "Blueberries"
    }
]

with app.app_context():
    for item in aliases:

        food = db.session.execute(
            db.select(Food)
                .where(
                Food.food_name == item["food"]
            )
        ).scalar_one_or_none()

        if food:
            alias = FoodAlias(
                search_term=item["search"],
                food_id=food.id,
                display_name=food.food_name
            )

            db.session.add(alias)

    db.session.commit()

print("Food aliases added")
