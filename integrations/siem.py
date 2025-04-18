import requests

class SIEMIntegration:
    """Intégration simple avec un SIEM via une API REST."""

    def __init__(self, endpoint, api_key=None):
        self.endpoint = endpoint
        self.api_key = api_key

    def send_alert(self, alert):
        """
        Envoie une alerte au SIEM.
        Args:
            alert (dict): Dictionnaire représentant l'alerte à envoyer.
        Returns:
            dict: Résultat de l'envoi.
        """
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        try:
            response = requests.post(self.endpoint, json=alert, headers=headers, timeout=5)
            return {"status": response.status_code, "response": response.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}