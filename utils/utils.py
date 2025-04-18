import logging
import json

def setup_logger(name="ghostnet", level=logging.INFO):
    """Configure et retourne un logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger

def load_config(path):
    """Charge un fichier de configuration JSON."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

def save_config(path, config):
    """Sauvegarde la configuration dans un fichier JSON."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}