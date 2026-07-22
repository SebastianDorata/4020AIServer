from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired


# Form for collecting user information to generate a nutrition plan
class DietForm(FlaskForm):

    age = IntegerField(
        "Age",
        validators=[DataRequired()]
    )

    gender = SelectField(
        "Gender",
        choices=[
            ("male", "Male"),
            ("female", "Female")
        ],
        validators=[DataRequired()]
    )

    height = SelectField(
        "Height",
        choices=[
            (str(i), f"{i // 12} ft {i % 12} in")
            for i in range(48, 86)  # 4'0" through 7'0"
        ],
        validators=[DataRequired()]
    )

    weight = FloatField(
        "Weight (lbs)",
        validators=[DataRequired()]
    )

    activity = SelectField(
        "Activity Level",
        choices=[
            ("1.2", "Sedentary (office job)"),
            ("1.375", "Light Exercise (1-2 days/week)"),
            ("1.55", "Moderate Exercise (3-5 days/week)"),
            ("1.725", "Heavy Exercise (6-7 days/week)"),
            ("1.9", "Athlete (2x per day)")
        ],
        validators=[DataRequired()]
    )

    goal = SelectField(
        "Goal",
        choices=[
            ("lose", "Lose Weight"),
            ("maintain", "Maintain Weight"),
            ("gain", "Gain Weight")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Generate Plan")