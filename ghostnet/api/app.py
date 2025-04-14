#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API REST pour GhostNet.

Ce module fournit une interface REST pour interagir avec le système GhostNet,
permettant de contrôler les honeypots, récupérer les données de détection
et gérer la configuration.
"""

from flask import Flask, jsonify, request, abort
from flask_restful import Api, Resource
from flask_cors import CORS
import os
import sys
import yaml
import logging
import datetime
import json
from typing import Dict, List, Any, Optional, Union

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler("logs/api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ghostnet.api")

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Activer CORS pour toutes les routes
api = Api(app)

# Charger la configuration
def load_config(config_path: str) -> dict:
    """
    Charge la configuration depuis un fichier YAML.
    
    Args:
        config_path: Chemin vers le fichier de configuration
        
    Returns:
        Dictionnaire de configuration
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Configuration chargée depuis {config_path}")
        return config
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la configuration: {e}")
        return {}

# Configuration par défaut
DEFAULT_CONFIG_PATH = os.environ.get("GHOSTNET_CONFIG", "config/config.yaml")
config = load_config(DEFAULT_CONFIG_PATH)

# Fonctions utilitaires pour l'API
def get_api_config() -> dict:
    """
    Récupère la configuration de l'API.
    
    Returns:
        Configuration de l'API
    """
    return {
        "port": config.get("general", {}).get("api_port", 8080),
        "host": config.get("general", {}).get("api_host", "0.0.0.0"),
        "ssl": config.get("general", {}).get("enable_ssl", False),
        "ssl_cert": config.get("general", {}).get("ssl_cert", ""),
        "ssl_key": config.get("general", {}).get("ssl_key", "")
    }

def validate_auth(request) -> bool:
    """
    Valide l'authentification de la requête.
    
    Args:
        request: Requête Flask
        
    Returns:
        True si l'authentification est valide, False sinon
    """
    # TODO: Implémenter la vérification d'authentification réelle
    # Pour l'instant, on accepte toutes les requêtes
    return True

# Ressources API
class StatusResource(Resource):
    """Ressource pour vérifier le statut du système."""
    
    def get(self):
        """
        Récupère le statut du système.
        
        Returns:
            Dictionnaire avec les informations de statut
        """
        if not validate_auth(request):
            abort(401, description="Non autorisé")
            
        return jsonify({
            "status": "online",
            "version": config.get("general", {}).get("version", "1.0.0"),
            "uptime": "TODO",  # À implémenter
            "modules": {
                "detection": config.get("detection", {}).get("enabled", True),
                "lure_generator": config.get("lure_generator", {}).get("enabled", True),
                "ai_engine": config.get("ai_engine", {}).get("enabled", True),
            },
            "timestamp": datetime.datetime.now().isoformat()
        })

class AlertsResource(Resource):
    """Ressource pour accéder aux alertes de sécurité."""
    
    def get(self):
        """
        Récupère les alertes de sécurité.
        
        Returns:
            Liste des alertes
        """
        if not validate_auth(request):
            abort(401, description="Non autorisé")
            
        # TODO: Récupérer les alertes depuis le système de stockage
        # Pour l'instant, on retourne un exemple
        return jsonify({
            "alerts": [
                {
                    "id": "alert-001",
                    "timestamp": "2025-04-14T12:00:00Z",
                    "severity": "high",
                    "source_ip": "192.168.1.100",
                    "type": "ssh_bruteforce",
                    "description": "Tentative de force brute SSH détectée",
                    "details": {
                        "attempts": 15,
                        "username": "root",
                        "duration": 120
                    }
                }
            ],
            "total": 1,
            "page": 1,
            "page_size": 10
        })

class ConfigResource(Resource):
    """Ressource pour gérer la configuration."""
    
    def get(self):
        """
        Récupère la configuration actuelle.
        
        Returns:
            Configuration actuelle
        """
        if not validate_auth(request):
            abort(401, description="Non autorisé")
            
        # On ne renvoie pas les informations sensibles
        safe_config = {
            "general": config.get("general", {}),
            "detection": config.get("detection", {}),
            "lure_generator": config.get("lure_generator", {}),
            "network_manager": config.get("network_manager", {}),
            "ai_engine": config.get("ai_engine", {}),
            "reporting": config.get("reporting", {})
        }
        
        # Supprimer les clés sensibles
        if "ssl_key" in safe_config.get("general", {}):
            safe_config["general"]["ssl_key"] = "***"
        
        return jsonify(safe_config)

class LuresResource(Resource):
    """Ressource pour gérer les leurres."""
    
    def get(self):
        """
        Récupère la liste des leurres actifs.
        
        Returns:
            Liste des leurres actifs
        """
        if not validate_auth(request):
            abort(401, description="Non autorisé")
            
        # TODO: Récupérer les leurres depuis le générateur de leurres
        # Pour l'instant, on retourne un exemple
        return jsonify({
            "lures": [
                {
                    "id": "lure-001",
                    "name": "SSH Server",
                    "status": "active",
                    "type": "service",
                    "service": "ssh",
                    "port": 22,
                    "created_at": "2025-04-14T10:00:00Z"
                },
                {
                    "id": "lure-002",
                    "name": "Web Server",
                    "status": "active",
                    "type": "service",
                    "service": "http",
                    "port": 80,
                    "created_at": "2025-04-14T10:05:00Z"
                }
            ],
            "total": 2
        })
    
    def post(self):
        """
        Crée un nouveau leurre.
        
        Returns:
            Informations sur le leurre créé
        """
        if not validate_auth(request):
            abort(401, description="Non autorisé")
            
        data = request.get_json()
        if not data:
            abort(400, description="Données JSON requises")
            
        # Validation des données
        required_fields = ["name", "type", "service"]
        for field in required_fields:
            if field not in data:
                abort(400, description=f"Champ requis manquant: {field}")
        
        # TODO: Créer le leurre via le générateur de leurres
        # Pour l'instant, on retourne un exemple
        new_lure = {
            "id": "lure-003",
            "name": data["name"],
            "status": "active",
            "type": data["type"],
            "service": data["service"],
            "port": data.get("port", 0),
            "created_at": datetime.datetime.now().isoformat()
        }
        
        logger.info(f"Nouveau leurre créé: {new_lure['id']}")
        return jsonify(new_lure), 201

class LureDetailResource(Resource):
    """Ressource pour gérer un leurre spécifique."""
    
    def get(self, lure_id):
        """
        Récupère les détails d'un leurre.
        
        Args:
            lure_id: Identifiant du leurre
            
        Returns:
            Détails du leurre
        """
        if not validate_auth(request):
            abort(401, description="Non autorisé")
            
        # TODO: Récupérer le leurre depuis le générateur de leurres
        # Pour l'instant, on retourne un exemple
        if lure_id == "lure-001":
            return jsonify({
                "id": "lure-001",
                "name": "SSH Server",
                "status": "active",
                "type": "service",
                "service": "ssh",
                "port": 22,
                "created_at": "2025-04-14T10:00:00Z",
                "stats": {
                    "connections": 15,
                    "last_connection": "2025-04-14T15:30:00Z",
                    "unique_ips": 3
                },
                "configuration": {
                    "banner": "OpenSSH 8.2p1 Ubuntu",
                    "credentials": [
                        {"username": "root", "password": "password123"},
                        {"username": "admin", "password": "admin123"}
                    ]
                }
            })
        else:
            abort(404, description="Leurre non trouvé")
    
    def put(self, lure_id):
        """
        Met à jour un leurre.
        
        Args:
            lure_id: Identifiant du leurre
            
        Returns:
            Leurre mis à jour
        """
        if not validate_auth(request):
            abort(401, description="Non autorisé")
            
        data = request.get_json()
        if not data:
            abort(400, description="Données JSON requises")
            
        # TODO: Mettre à jour le leurre via le générateur de leurres
        # Pour l'instant, on retourne un exemple
        if lure_id == "lure-001":
            updated_lure = {
                "id": "lure-001",
                "name": data.get("name", "SSH Server"),
                "status": data.get("status", "active"),
                "type": "service",
                "service": "ssh",
                "port": data.get("port", 22),
                "created_at": "2025-04-14T10:00:00Z",
                "updated_at": datetime.datetime.now().isoformat()
            }
            logger.info(f"Leurre mis à jour: {lure_id}")
            return jsonify(updated_lure)
        else:
            abort(404, description="Leurre non trouvé")
    
    def delete(self, lure_id):
        """
        Supprime un leurre.
        
        Args:
            lure_id: Identifiant du leurre
            
        Returns:
            Confirmation de suppression
        """
        if not validate_auth(request):
            abort(401, description="Non autorisé")
            
        # TODO: Supprimer le leurre via le générateur de leurres
        # Pour l'instant, on retourne un exemple
        if lure_id in ["lure-001", "lure-002"]:
            logger.info(f"Leurre supprimé: {lure_id}")
            return jsonify({"message": f"Leurre {lure_id} supprimé avec succès"}), 200
        else:
            abort(404, description="Leurre non trouvé")

class AttackersResource(Resource):
    """Ressource pour accéder aux informations sur les attaquants."""
    
    def get(self):
        """
        Récupère la liste des attaquants détectés.
        
        Returns:
            Liste des attaquants
        """
        if not validate_auth(request):
            abort(401, description="Non autorisé")
            
        # TODO: Récupérer les attaquants depuis le système de stockage
        # Pour l'instant, on retourne un exemple
        return jsonify({
            "attackers": [
                {
                    "ip": "192.168.1.100",
                    "first_seen": "2025-04-14T12:00:00Z",
                    "last_seen": "2025-04-14T15:30:00Z",
                    "attacks": 15,
                    "types": ["ssh_bruteforce", "port_scan"],
                    "severity": "high",
                    "geo": {
                        "country": "Unknown",
                        "city": "Unknown",
                        "coordinates": [0, 0]
                    }
                }
            ],
            "total": 1,
            "page": 1,
            "page_size": 10
        })

class ReportsResource(Resource):
    """Ressource pour générer et accéder aux rapports."""
    
    def get(self):
        """
        Récupère la liste des rapports disponibles.
        
        Returns:
            Liste des rapports
        """
        if not validate_auth(request):
            abort(401, description="Non autorisé")
            
        # TODO: Récupérer les rapports depuis le système de stockage
        # Pour l'instant, on retourne un exemple
        return jsonify({
            "reports": [
                {
                    "id": "report-001",
                    "name": "Rapport journalier - 2025-04-13",
                    "type": "daily",
                    "format": "pdf",
                    "created_at": "2025-04-14T00:00:00Z",
                    "url": "/api/reports/report-001/download"
                }
            ],
            "total": 1
        })
    
    def post(self):
        """
        Génère un nouveau rapport.
        
        Returns:
            Informations sur le rapport généré
        """
        if not validate_auth(request):
            abort(401, description="Non autorisé")
            
        data = request.get_json()
        if not data:
            abort(400, description="Données JSON requises")
            
        # Validation des données
        required_fields = ["type", "period"]
        for field in required_fields:
            if field not in data:
                abort(400, description=f"Champ requis manquant: {field}")
        
        # TODO: Générer le rapport via le système de reporting
        # Pour l'instant, on retourne un exemple
        new_report = {
            "id": "report-002",
            "name": f"Rapport {data['type']} - {data['period']}",
            "type": data["type"],
            "period": data["period"],
            "format": data.get("format", "pdf"),
            "created_at": datetime.datetime.now().isoformat(),
            "status": "generating"
        }
        
        logger.info(f"Nouveau rapport généré: {new_report['id']}")
        return jsonify(new_report), 202  # Accepted

# Enregistrement des routes
api.add_resource(StatusResource, "/api/status")
api.add_resource(AlertsResource, "/api/alerts")
api.add_resource(ConfigResource, "/api/config")
api.add_resource(LuresResource, "/api/lures")
api.add_resource(LureDetailResource, "/api/lures/<string:lure_id>")
api.add_resource(AttackersResource, "/api/attackers")
api.add_resource(ReportsResource, "/api/reports")

# Point d'entrée principal pour servir l'API
def main():
    """
    Point d'entrée principal pour démarrer le serveur API.
    """
    api_config = get_api_config()
    
    # Configurer le niveau de journalisation
    log_level = config.get("general", {}).get("log_level", "INFO")
    numeric_level = getattr(logging, log_level.upper(), None)
    if isinstance(numeric_level, int):
        logger.setLevel(numeric_level)
    
    # Afficher les informations de démarrage
    logger.info(f"Démarrage de l'API GhostNet sur {api_config['host']}:{api_config['port']}")
    logger.info(f"SSL: {'Activé' if api_config['ssl'] else 'Désactivé'}")
    
    # Démarrer le serveur avec ou sans SSL
    if api_config["ssl"]:
        ssl_context = (api_config["ssl_cert"], api_config["ssl_key"])
        app.run(
            host=api_config["host"],
            port=api_config["port"],
            ssl_context=ssl_context,
            debug=False
        )
    else:
        app.run(
            host=api_config["host"],
            port=api_config["port"],
            debug=False
        )

if __name__ == "__main__":
    main()
