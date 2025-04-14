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
