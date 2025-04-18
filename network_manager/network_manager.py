import socket

class NetworkManager:
    """Gère les interactions réseau et le déploiement des leurres."""

    def __init__(self):
        self.active_lures = []

    def deploy_lure(self, ip="127.0.0.1", port=8080):
        """Déploie un leurre réseau (exemple : ouvre un port factice)."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((ip, port))
            s.listen(1)
            self.active_lures.append({"ip": ip, "port": port, "socket": s})
            return {"status": "success", "ip": ip, "port": port}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_active_lures(self):
        """Liste les leurres réseau actifs."""
        return [{"ip": l["ip"], "port": l["port"]} for l in self.active_lures]

    def close_all_lures(self):
        """Ferme tous les leurres réseau actifs."""
        for lure in self.active_lures:
            lure["socket"].close()
        self.active_lures = []
        return {"status": "all lures closed"}