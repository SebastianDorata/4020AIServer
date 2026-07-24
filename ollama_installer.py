import os
import time
from ollama import Client, ResponseError


def initialize_ollama_model():
    """
    Verifies connection to the Ollama server and automatically
    downloads the target LLM model if it is missing.
    """
    # 1. Read variables dynamically from environment setup
    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    model_name = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")

    print(f"Connecting to Ollama engine at: {ollama_host}...")
    client = Client(host=ollama_host)

    # 2. Wait loop to ensure Ollama container/service is fully booted up
    max_retries = 10
    for attempt in range(max_retries):
        try:
            # Test connection by requesting local model tags
            client.list()
            break
        except Exception:
            if attempt == max_retries - 1:
                print("❌ Error: Could not connect to Ollama service. Is it running?")
                return False
            print(f"⏳ Waiting for Ollama engine to initialize (Attempt {attempt + 1}/{max_retries})...")
            time.sleep(3)

    # 3. Check if target model exists locally
    try:
        print(f"Checking for model profile: '{model_name}'...")
        # Use built-in SDK logic to see if model exists
        client.show(model_name)
        print(f"✅ Model '{model_name}' is verified and ready for execution.")
        return True
    except ResponseError as e:
        # Status code 404 indicates the server is active, but the model hasn't been pulled yet
        if e.status_code == 404:
            print(f"📥 Model '{model_name}' not found. Initializing automated download stream...")
            try:
                # Stream the pull status directly to the console logs
                current_status = ""
                for progress in client.pull(model=model_name, stream=True):
                    status = progress.get('status', '')
                    if status != current_status:
                        print(f" -> {status}")
                        current_status = status
                print(f"✅ Successfully downloaded and compiled '{model_name}'!")
                return True
            except Exception as pull_err:
                print(f"❌ Failed to download model: {pull_err}")
                return False
        else:
            print(f"❌ Server communication error: {e}")
            return False


if __name__ == "__main__":
    initialize_ollama_model()
