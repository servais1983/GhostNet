import random

class AIEngine:
    """Moteur d'IA pour l'analyse avancée et le scoring des événements."""

    def __init__(self):
        pass

    def score_event(self, event):
        """
        Attribue un score de risque à un événement.
        Args:
            event (dict): Dictionnaire représentant un événement.
        Returns:
            dict: Résultat avec score et niveau de risque.
        """
        # Exemple simple : score aléatoire
        score = random.randint(1, 100)
        if score > 80:
            niveau = "critique"
        elif score > 50:
            niveau = "élevé"
        elif score > 20:
            niveau = "moyen"
        else:
            niveau = "faible"
        return {"event": event, "score": score, "niveau": niveau}

    def correlate_events(self, events):
        """
        Corrèle une liste d'événements pour détecter des attaques complexes.
        Args:
            events (list): Liste de dictionnaires d'événements.
        Returns:
            dict: Résultat de la corrélation.
        """
        # Exemple : si plus de 3 événements du même type, alerte corrélée
        types = [e.get("type") for e in events]
        for t in set(types):
            if types.count(t) > 3:
                return {"correlated": True, "type": t, "message": "Alerte corrélée détectée"}
        return {"correlated": False}