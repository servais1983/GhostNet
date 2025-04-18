class SignatureDetector:
    """Détecteur par signature pour identifier des attaques connues."""
    def __init__(self):
        # Exemple de signatures connues
        self.signatures = [
            {"id": 1, "pattern": "Failed password", "description": "Tentative de connexion SSH échouée"},
            {"id": 2, "pattern": "SQL injection", "description": "Tentative d'injection SQL"}
        ]

    def analyze(self, log_entry):
        """Analyse une entrée de log et retourne une alerte si une signature est détectée."""
        for sig in self.signatures:
            if sig["pattern"].lower() in log_entry.lower():
                return {
                    "detected": True,
                    "type": "signature",
                    "description": sig["description"]
                }
        return {"detected": False}