class BehavioralDetector:
    """Détecteur comportemental (exemple simple)."""
    def __init__(self):
        self.user_activity = {}

    def analyze(self, user, action):
        """Détecte des comportements inhabituels pour un utilisateur."""
        if user not in self.user_activity:
            self.user_activity[user] = []
        self.user_activity[user].append(action)
        # Exemple : si un utilisateur fait 3 actions différentes en moins d'une minute
        if len(set(self.user_activity[user][-3:])) == 3:
            return {
                "detected": True,
                "type": "behavioral",
                "description": f"Comportement inhabituel détecté pour {user}"
            }
        return {"detected": False}