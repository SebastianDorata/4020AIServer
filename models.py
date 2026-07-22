from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, ForeignKey


# Base class for all database models
class Base(DeclarativeBase):
    pass


# Food nutrition database table
# Nutrition values are stored per 100 grams
class Food(Base):
    __tablename__ = "foods"

    # Food ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Name of food item
    food_name: Mapped[str] = mapped_column(String(400), nullable=False)

    # Calories per 100 grams
    calories: Mapped[float] = mapped_column(Float, nullable=False)

    # Macronutrients per 100 grams
    fat: Mapped[float] = mapped_column(Float, nullable=False)

    carbs: Mapped[float] = mapped_column(Float, nullable=False)

    protein: Mapped[float] = mapped_column(Float, nullable=False)

# Mapping table for ai to connect food aliases with real food items in the database.
class FoodAlias(Base):
    __tablename__ = "food_aliases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # What the AI/user says
    search_term: Mapped[str] = mapped_column(String(100), nullable=False)

    # Exact name in foods table
    food_id: Mapped[int] = mapped_column(
        ForeignKey("foods.id"),
        nullable=False
    )

    # Optional: makes debugging easier
    display_name: Mapped[str] = mapped_column(
        String(400),
        nullable=False
    )