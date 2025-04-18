from detection import SignatureDetector, AnomalyDetector, BehavioralDetector
from lure_generator import LureGenerator
from network_manager import NetworkManager
from ai_engine import AIEngine
from integrations import SIEMIntegration
from utils import setup_logger, load_config
from database import DatabaseManager

logger = setup_logger()
config = load_config("config/default_config.json")
db = DatabaseManager()
ai_engine = AIEngine()
lure_gen = LureGenerator()
network_mgr = NetworkManager()
siem = SIEMIntegration(config.get("siem_endpoint", ""), None)

# Exemple d'orchestration
def traiter_evenement(log_entry, user=None, action=None):
    logger.info("Analyse de l'événement : %s", log_entry)
    signature = SignatureDetector().analyze(log_entry)
    if signature["detected"]:
        logger.warning("Détection par signature : %s", signature["description"])
        db.insert_alerte("signature", "élevé", signature["description"])
        siem.send_alert(signature)
        return signature

    if user and action:
        comportement = BehavioralDetector().analyze(user, action)
        if comportement["detected"]:
            logger.warning("Détection comportementale : %s", comportement["description"])
            db.insert_alerte("behavioral", "moyen", comportement["description"])
            siem.send_alert(comportement)
            return comportement

    # Exemple d'analyse IA
    score = ai_engine.score_event({"log": log_entry})
    logger.info("Score IA : %s", score)
    if score["niveau"] in ["élevé", "critique"]:
        db.insert_alerte("ai", score["niveau"], "Score IA élevé")
        siem.send_alert(score)
        return score

    logger.info("Aucune menace détectée.")
    return {"detected": False}

if __name__ == "__main__":
    # Exemple d'utilisation
    traiter_evenement("Tentative de connexion SSH échouée: Failed password", user="alice", action="login")