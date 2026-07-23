from flask import Flask
from flask_bootstrap import Bootstrap5
import logging
from db import db
from routes import route_controller


# Create Flask application
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
# Flask configuration
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nutrition.db"


# Initialize Flask extensions
Bootstrap5(app)
db.init_app(app)


# Register Blueprint routes
app.register_blueprint(route_controller)


# Create database tables if they do not exist
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True, port=5001)