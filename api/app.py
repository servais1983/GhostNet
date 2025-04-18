from flask import Flask, jsonify, request

app = Flask(__name__)

# Exemple de configuration en mémoire
CONFIG = {
    "mode": "défaut",
    "alert_threshold": 5
}

ALERTES = [
    {"id": 1, "type": "intrusion", "niveau": "élevé", "message": "Intrusion détectée sur le port 22."}
]

@app.route('/api/config', methods=['GET', 'POST'])
def config():
    if request.method == 'GET':
        return jsonify(CONFIG)
    elif request.method == 'POST':
        data = request.json
        CONFIG.update(data)
        return jsonify({"status": "ok", "config": CONFIG})

@app.route('/api/alertes', methods=['GET'])
def alertes():
    return jsonify(ALERTES)

@app.route('/api/gestion', methods=['POST'])
def gestion():
    action = request.json.get("action")
    # Ici, tu peux ajouter la logique de gestion (ex: démarrer/arrêter modules)
    return jsonify({"status": "action reçue", "action": action})

if __name__ == '__main__':
    app.run(debug=True)