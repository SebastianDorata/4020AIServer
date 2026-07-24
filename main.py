from flask import Flask
from flask_bootstrap import Bootstrap5
import logging
from db import db
from routes import route_controller
import atexit
import os
import subprocess
import time
import requests

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


def ensure_ollama_and_model():
    """
    Universally ensures Ollama is running and that the model is downloaded.
    Works natively on bare-metal MacOS and inside Docker setups.
    """
    # 1. Fetch environment values or fallback to local defaults
    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip('/')
    model_name = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")
    is_docker = os.environ.get("RUNNING_IN_DOCKER") or os.path.exists('/.dockerenv')

    # 2. Check connection loop
    connected = False
    max_retries = 3

    for attempt in range(max_retries):
        try:
            requests.get(f"{ollama_host}/api/tags", timeout=3)
            connected = True
            break
        except requests.exceptions.RequestException:
            # If bare metal Mac and not running, attempt Homebrew launch once
            if not is_docker and attempt == 0:
                print("Ollama isn't running — starting via Homebrew...")
                try:
                    subprocess.run(["brew", "services", "start", "ollama"], check=True)
                    # Register shutdown only if running locally on bare metal
                    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
                        atexit.register(stop_ollama_local)
                except Exception as e:
                    print(f"Could not automatically start Homebrew Ollama: {e}")

            print(f"⏳ Waiting for Ollama engine at {ollama_host} (Attempt {attempt + 1}/{max_retries})...")
            time.sleep(4)

    if not connected:
        print(f" Error: Cannot connect to Ollama service at {ollama_host}.")
        return

    # 3. Model download validation check
    try:
        print(f"Verifying local presence of model: '{model_name}'...")
        check_resp = requests.post(f"{ollama_host}/api/show", json={"name": model_name}, timeout=5)

        if check_resp.status_code == 200:
            print(f" Model '{model_name}' is verified and active.")
        else:
            # Model is missing (404), trigger stream pull download
            print(f" Model '{model_name}' not found. Initializing automated download...")
            pull_resp = requests.post(f"{ollama_host}/api/pull", json={"name": model_name}, stream=True, timeout=None)

            for line in pull_resp.iter_lines():
                if line:
                    print(f" -> {line.decode('utf-8')}")
            print(f" Successfully pulled '{model_name}'!")

    except Exception as err:
        print(f" Error verifying or downloading the model payload: {err}")


def stop_ollama_local():
    """Stops the native Homebrew service if running on host machine."""
    print("Stopping local Homebrew Ollama...")
    subprocess.run(["brew", "services", "stop", "ollama"], check=False)


if __name__ == "__main__":
    # Ensure Ollama and models are completely set up before starting Flask web app
    ensure_ollama_and_model()

    # Bind to 0.0.0.0 inside Docker so the port mapping actually works;
    # keep it to localhost when running bare-metal for a bit of extra safety
    is_docker = os.environ.get("RUNNING_IN_DOCKER") or os.path.exists('/.dockerenv')
    host = "0.0.0.0" if is_docker else "127.0.0.1"

    # Disable reloader to prevent duplicate initialization blocks
    app.run(host=host, debug=True, use_reloader=False, port=5001)
