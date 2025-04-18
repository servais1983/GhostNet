import random

class LureGenerator:
    """Génère des leurres (fichiers, services, endpoints factices)."""

    def __init__(self):
        self.lures = []

    def generate_file_lure(self, filename="fake_document.txt"):
        """Crée un fichier leurre factice."""
        content = f"Ce fichier {filename} est un leurre généré automatiquement."
        self.lures.append({"type": "file", "name": filename, "content": content})
        return {"filename": filename, "content": content}

    def generate_service_lure(self, port=None):
        """Simule un service leurre sur un port donné."""
        if port is None:
            port = random.randint(1024, 65535)
        self.lures.append({"type": "service", "port": port})
        return {"service": "fake_service", "port": port}

    def list_lures(self):
        """Retourne la liste des leurres générés."""
        return self.lures