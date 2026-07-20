from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


# Base class for all database models
class Base(DeclarativeBase):
    pass


# Food nutrition database table
# Nutrition values are stored per 100 grams
class Food(Base):
    __tablename__ = "food"

    # Food ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Name of food item
    food_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Calories per 100 grams
    calories: Mapped[float] = mapped_column(Float, nullable=False)

    # Macronutrients per 100 grams
    fat: Mapped[float] = mapped_column(Float, nullable=False)

    carbs: Mapped[float] = mapped_column(Float, nullable=False)

    protein: Mapped[float] = mapped_column(Float, nullable=False)

    fiber: Mapped[float] = mapped_column(Float, nullable=False)