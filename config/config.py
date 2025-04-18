import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "default_config.json")

def load_default_config():
    """Charge la configuration par défaut du projet."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}