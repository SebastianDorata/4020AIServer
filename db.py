from flask_sqlalchemy import SQLAlchemy
from models import Base

# DB import maintaining MCV architecture

db = SQLAlchemy(model_class=Base)