class AnomalyDetector:
    """Détecteur d'anomalies basé sur des seuils simples."""
    def __init__(self, threshold=10):
        self.threshold = threshold

    def analyze(self, event_count):
        """Détecte une anomalie si le nombre d'événements dépasse le seuil."""
        if event_count > self.threshold:
            return {
                "detected": True,
                "type": "anomaly",
                "description": f"Nombre d'événements anormalement élevé : {event_count}"
            }
        return {"detected": False}