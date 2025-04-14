#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module d'intégration avec les SIEM pour GhostNet.

Ce module permet d'envoyer les alertes et les événements générés par GhostNet
vers différents SIEM (Security Information and Event Management).
"""

import os
import sys
import json
import logging
import datetime
from typing import Dict, List, Any, Optional, Union
import requests
from abc import ABC, abstractmethod

# Configuration des logs
logger = logging.getLogger("ghostnet.integrations.siem")

class SIEMIntegration(ABC):
    """
    Classe abstraite pour l'intégration avec un SIEM.
    """
    
    @abstractmethod
    def send_event(self, event: Dict[str, Any]) -> bool:
        """
        Envoie un événement au SIEM.
        
        Args:
            event: Dictionnaire contenant les informations de l'événement
            
        Returns:
            True si l'événement a été envoyé avec succès, False sinon
        """
        pass
    
    @abstractmethod
    def send_alert(self, alert: Dict[str, Any]) -> bool:
        """
        Envoie une alerte au SIEM.
        
        Args:
            alert: Dictionnaire contenant les informations de l'alerte
            
        Returns:
            True si l'alerte a été envoyée avec succès, False sinon
        """
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """
        Teste la connexion avec le SIEM.
        
        Returns:
            True si la connexion est établie avec succès, False sinon
        """
        pass

class ElasticSIEM(SIEMIntegration):
    """
    Intégration avec Elasticsearch/Elastic SIEM.
    """
    
    def __init__(self, host: str, port: int, index: str, username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialise l'intégration avec Elasticsearch.
        
        Args:
            host: Hôte Elasticsearch
            port: Port Elasticsearch
            index: Index Elasticsearch pour les données GhostNet
            username: Nom d'utilisateur (optionnel)
            password: Mot de passe (optionnel)
        """
        self.host = host
        self.port = port
        self.index = index
        self.username = username
        self.password = password
        self.base_url = f"http://{host}:{port}"
        
        # Authentification
        self.auth = None
        if username and password:
            self.auth = (username, password)
        
        logger.info(f"Intégration Elasticsearch initialisée: {host}:{port}/{index}")
    
    def send_event(self, event: Dict[str, Any]) -> bool:
        """
        Envoie un événement à Elasticsearch.
        
        Args:
            event: Dictionnaire contenant les informations de l'événement
            
        Returns:
            True si l'événement a été envoyé avec succès, False sinon
        """
        try:
            # Ajouter un timestamp si non présent
            if "timestamp" not in event:
                event["timestamp"] = datetime.datetime.now().isoformat()
            
            # Ajouter un type d'événement si non présent
            if "type" not in event:
                event["type"] = "ghostnet_event"
            
            url = f"{self.base_url}/{self.index}/_doc"
            response = requests.post(url, json=event, auth=self.auth)
            
            if response.status_code in [200, 201]:
                logger.debug(f"Événement envoyé à Elasticsearch: {response.json()}")
                return True
            else:
                logger.error(f"Erreur lors de l'envoi de l'événement à Elasticsearch: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Exception lors de l'envoi de l'événement à Elasticsearch: {e}")
            return False
    
    def send_alert(self, alert: Dict[str, Any]) -> bool:
        """
        Envoie une alerte à Elasticsearch.
        
        Args:
            alert: Dictionnaire contenant les informations de l'alerte
            
        Returns:
            True si l'alerte a été envoyée avec succès, False sinon
        """
        try:
            # Ajouter un timestamp si non présent
            if "timestamp" not in alert:
                alert["timestamp"] = datetime.datetime.now().isoformat()
            
            # Ajouter un type d'alerte
            alert["type"] = "ghostnet_alert"
            
            url = f"{self.base_url}/{self.index}/_doc"
            response = requests.post(url, json=alert, auth=self.auth)
            
            if response.status_code in [200, 201]:
                logger.debug(f"Alerte envoyée à Elasticsearch: {response.json()}")
                return True
            else:
                logger.error(f"Erreur lors de l'envoi de l'alerte à Elasticsearch: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Exception lors de l'envoi de l'alerte à Elasticsearch: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        Teste la connexion avec Elasticsearch.
        
        Returns:
            True si la connexion est établie avec succès, False sinon
        """
        try:
            url = f"{self.base_url}/_cluster/health"
            response = requests.get(url, auth=self.auth)
            
            if response.status_code == 200:
                logger.info(f"Connexion à Elasticsearch établie: {response.json()}")
                return True
            else:
                logger.error(f"Erreur lors de la connexion à Elasticsearch: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Exception lors de la connexion à Elasticsearch: {e}")
            return False

class SplunkSIEM(SIEMIntegration):
    """
    Intégration avec Splunk SIEM.
    """
    
    def __init__(self, host: str, port: int, token: str, index: str = "ghostnet"):
        """
        Initialise l'intégration avec Splunk.
        
        Args:
            host: Hôte Splunk
            port: Port Splunk HTTP Event Collector
            token: Token d'authentification HTTP Event Collector
            index: Index Splunk pour les données GhostNet
        """
        self.host = host
        self.port = port
        self.token = token
        self.index = index
        self.base_url = f"https://{host}:{port}/services/collector"
        
        logger.info(f"Intégration Splunk initialisée: {host}:{port}")
    
    def send_event(self, event: Dict[str, Any]) -> bool:
        """
        Envoie un événement à Splunk.
        
        Args:
            event: Dictionnaire contenant les informations de l'événement
            
        Returns:
            True si l'événement a été envoyé avec succès, False sinon
        """
        try:
            # Format attendu par Splunk HEC
            data = {
                "time": int(datetime.datetime.now().timestamp()),
                "host": "ghostnet",
                "source": "ghostnet_events",
                "sourcetype": "ghostnet_event",
                "index": self.index,
                "event": event
            }
            
            headers = {
                "Authorization": f"Splunk {self.token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(self.base_url, json=data, headers=headers, verify=False)
            
            if response.status_code == 200:
                resp_json = response.json()
                if resp_json.get("text") == "Success":
                    logger.debug(f"Événement envoyé à Splunk: {resp_json}")
                    return True
                else:
                    logger.error(f"Erreur lors de l'envoi de l'événement à Splunk: {resp_json}")
                    return False
            else:
                logger.error(f"Erreur lors de l'envoi de l'événement à Splunk: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Exception lors de l'envoi de l'événement à Splunk: {e}")
            return False
    
    def send_alert(self, alert: Dict[str, Any]) -> bool:
        """
        Envoie une alerte à Splunk.
        
        Args:
            alert: Dictionnaire contenant les informations de l'alerte
            
        Returns:
            True si l'alerte a été envoyée avec succès, False sinon
        """
        try:
            # Format attendu par Splunk HEC
            data = {
                "time": int(datetime.datetime.now().timestamp()),
                "host": "ghostnet",
                "source": "ghostnet_alerts",
                "sourcetype": "ghostnet_alert",
                "index": self.index,
                "event": alert
            }
            
            headers = {
                "Authorization": f"Splunk {self.token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(self.base_url, json=data, headers=headers, verify=False)
            
            if response.status_code == 200:
                resp_json = response.json()
                if resp_json.get("text") == "Success":
                    logger.debug(f"Alerte envoyée à Splunk: {resp_json}")
                    return True
                else:
                    logger.error(f"Erreur lors de l'envoi de l'alerte à Splunk: {resp_json}")
                    return False
            else:
                logger.error(f"Erreur lors de l'envoi de l'alerte à Splunk: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Exception lors de l'envoi de l'alerte à Splunk: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        Teste la connexion avec Splunk.
        
        Returns:
            True si la connexion est établie avec succès, False sinon
        """
        try:
            # Envoyer un événement de test
            data = {
                "time": int(datetime.datetime.now().timestamp()),
                "host": "ghostnet",
                "source": "ghostnet_system",
                "sourcetype": "ghostnet_test",
                "index": self.index,
                "event": {"message": "Test de connexion GhostNet"}
            }
            
            headers = {
                "Authorization": f"Splunk {self.token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(self.base_url, json=data, headers=headers, verify=False)
            
            if response.status_code == 200:
                resp_json = response.json()
                if resp_json.get("text") == "Success":
                    logger.info("Connexion à Splunk établie avec succès")
                    return True
                else:
                    logger.error(f"Erreur lors de la connexion à Splunk: {resp_json}")
                    return False
            else:
                logger.error(f"Erreur lors de la connexion à Splunk: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Exception lors de la connexion à Splunk: {e}")
            return False

class SyslogSIEM(SIEMIntegration):
    """
    Intégration avec un serveur Syslog.
    """
    
    def __init__(self, host: str, port: int = 514, facility: str = "local0", protocol: str = "udp"):
        """
        Initialise l'intégration avec Syslog.
        
        Args:
            host: Hôte Syslog
            port: Port Syslog (défaut: 514)
            facility: Facility Syslog (défaut: local0)
            protocol: Protocole à utiliser (udp ou tcp, défaut: udp)
        """
        self.host = host
        self.port = port
        self.facility = facility
        self.protocol = protocol.lower()
        
        # Vérifier le protocole
        if self.protocol not in ["udp", "tcp"]:
            logger.warning(f"Protocole {protocol} non supporté, utilisation de UDP par défaut")
            self.protocol = "udp"
        
        logger.info(f"Intégration Syslog initialisée: {protocol}://{host}:{port}")
    
    def _send_syslog_message(self, message: str, severity: int = 5) -> bool:
        """
        Envoie un message au serveur Syslog.
        
        Args:
            message: Message à envoyer
            severity: Niveau de sévérité (0-7, défaut: 5/notice)
            
        Returns:
            True si le message a été envoyé avec succès, False sinon
        """
        try:
            import socket
            
            # Calculer la priorité (facility * 8 + severity)
            facility_code = {
                "kern": 0, "user": 1, "mail": 2, "daemon": 3,
                "auth": 4, "syslog": 5, "lpr": 6, "news": 7,
                "uucp": 8, "cron": 9, "authpriv": 10, "ftp": 11,
                "local0": 16, "local1": 17, "local2": 18, "local3": 19,
                "local4": 20, "local5": 21, "local6": 22, "local7": 23
            }.get(self.facility, 16)  # local0 par défaut
            
            priority = facility_code * 8 + severity
            
            # Formater le message selon RFC 5424
            timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            hostname = socket.gethostname()
            app_name = "ghostnet"
            proc_id = os.getpid()
            msg_id = "-"  # Non utilisé
            structured_data = "-"  # Non utilisé
            
            syslog_message = f"<{priority}>{timestamp} {hostname} {app_name} {proc_id} {msg_id} {structured_data} {message}"
            
            # Envoyer le message selon le protocole
            if self.protocol == "udp":
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(syslog_message.encode('utf-8'), (self.host, self.port))
                sock.close()
            else:  # TCP
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.host, self.port))
                sock.send(syslog_message.encode('utf-8'))
                sock.close()
            
            logger.debug(f"Message envoyé à Syslog: {syslog_message}")
            return True
        
        except Exception as e:
            logger.error(f"Exception lors de l'envoi du message à Syslog: {e}")
            return False
    
    def send_event(self, event: Dict[str, Any]) -> bool:
        """
        Envoie un événement au serveur Syslog.
        
        Args:
            event: Dictionnaire contenant les informations de l'événement
            
        Returns:
            True si l'événement a été envoyé avec succès, False sinon
        """
        try:
            # Sérialiser l'événement
            event_str = json.dumps(event)
            
            # Déterminer la sévérité
            severity = {
                "debug": 7,
                "info": 6,
                "notice": 5,
                "warning": 4,
                "error": 3,
                "critical": 2,
                "alert": 1,
                "emergency": 0
            }.get(event.get("severity", "").lower(), 6)  # Info par défaut
            
            # Préfixer le message pour indiquer qu'il s'agit d'un événement GhostNet
            message = f"GhostNet-Event: {event_str}"
            
            return self._send_syslog_message(message, severity)
        
        except Exception as e:
            logger.error(f"Exception lors de l'envoi de l'événement à Syslog: {e}")
            return False
    
    def send_alert(self, alert: Dict[str, Any]) -> bool:
        """
        Envoie une alerte au serveur Syslog.
        
        Args:
            alert: Dictionnaire contenant les informations de l'alerte
            
        Returns:
            True si l'alerte a été envoyée avec succès, False sinon
        """
        try:
            # Sérialiser l'alerte
            alert_str = json.dumps(alert)
            
            # Déterminer la sévérité
            severity = {
                "low": 5,
                "medium": 4,
                "high": 3,
                "critical": 2
            }.get(alert.get("severity", "").lower(), 3)  # High par défaut
            
            # Préfixer le message pour indiquer qu'il s'agit d'une alerte GhostNet
            message = f"GhostNet-Alert: {alert_str}"
            
            return self._send_syslog_message(message, severity)
        
        except Exception as e:
            logger.error(f"Exception lors de l'envoi de l'alerte à Syslog: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        Teste la connexion avec le serveur Syslog.
        
        Returns:
            True si la connexion est établie avec succès, False sinon
        """
        try:
            message = "GhostNet-Test: Test de connexion GhostNet"
            return self._send_syslog_message(message, 6)  # Info
        
        except Exception as e:
            logger.error(f"Exception lors de la connexion à Syslog: {e}")
            return False


# Factory pour créer l'intégration SIEM appropriée
def create_siem_integration(config: Dict[str, Any]) -> Optional[SIEMIntegration]:
    """
    Crée l'intégration SIEM appropriée en fonction de la configuration.
    
    Args:
        config: Configuration du SIEM
        
    Returns:
        Intégration SIEM appropriée ou None si la configuration est invalide
    """
    siem_type = config.get("type", "").lower()
    
    if siem_type == "elastic":
        return ElasticSIEM(
            host=config.get("host", "localhost"),
            port=config.get("port", 9200),
            index=config.get("index", "ghostnet"),
            username=config.get("username"),
            password=config.get("password")
        )
    
    elif siem_type == "splunk":
        return SplunkSIEM(
            host=config.get("host", "localhost"),
            port=config.get("port", 8088),
            token=config.get("token", ""),
            index=config.get("index", "ghostnet")
        )
    
    elif siem_type == "syslog":
        return SyslogSIEM(
            host=config.get("host", "localhost"),
            port=config.get("port", 514),
            facility=config.get("facility", "local0"),
            protocol=config.get("protocol", "udp")
        )
    
    else:
        logger.error(f"Type de SIEM non supporté: {siem_type}")
        return None
