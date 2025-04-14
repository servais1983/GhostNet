#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitaires pour le module de détection.
"""

import os
import sys
import pytest
import re
from unittest.mock import MagicMock, patch
from pathlib import Path

# Ajouter le répertoire parent au chemin d'importation
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Classes à tester (ces importations seront fonctionnelles une fois le code source créé)
# from ghostnet.detection.signature_detector import SignatureDetector
# from ghostnet.detection.anomaly_detector import AnomalyDetector
# from ghostnet.detection.behavioral_detector import BehavioralDetector
# from ghostnet.detection.engine import DetectionEngine

# Pour les tests, nous allons créer des mocks de ces classes
class MockSignatureRule:
    def __init__(self, name, pattern, count, timeframe, severity, action):
        self.name = name
        self.pattern = re.compile(pattern)
        self.count = count
        self.timeframe = timeframe
        self.severity = severity
        self.action = action

class MockSignatureDetector:
    def __init__(self, rules=None):
        self.rules = rules or []
    
    def load_rules(self, rules_config):
        self.rules = []
        for rule in rules_config:
            self.rules.append(MockSignatureRule(
                rule['name'],
                rule['pattern'],
                rule['count'],
                rule['timeframe'],
                rule['severity'],
                rule['action']
            ))
        return True
    
    def analyze(self, log_entries):
        results = []
        for rule in self.rules:
            matches = 0
            for entry in log_entries:
                if rule.pattern.search(entry):
                    matches += 1
            
            if matches >= rule.count:
                results.append({
                    "detected": True,
                    "rule_name": rule.name,
                    "severity": rule.severity,
                    "matches": matches,
                    "action": rule.action
                })
        
        return results[0] if results else {"detected": False}


class TestSignatureDetector:
    """Tests pour le détecteur basé sur les signatures."""
    
    def setup_method(self):
        """Initialisation avant chaque test."""
        self.detector = MockSignatureDetector()
        
        # Règles de test
        self.test_rules = [
            {
                "name": "SSH Brute Force",
                "pattern": r"Failed password for .* from .* port \d+ ssh2",
                "count": 5,
                "timeframe": 60,
                "severity": "high",
                "action": "redirect_to_lure"
            },
            {
                "name": "SQL Injection Attempt",
                "pattern": r"'(\s)*(or|OR)(\s)+.*=.*",
                "count": 1,
                "timeframe": 10,
                "severity": "critical",
                "action": "redirect_to_lure"
            }
        ]
        
        self.detector.load_rules(self.test_rules)
    
    def test_rule_loading(self):
        """Vérifier que les règles sont correctement chargées."""
        assert len(self.detector.rules) == 2
        assert self.detector.rules[0].name == "SSH Brute Force"
        assert self.detector.rules[1].name == "SQL Injection Attempt"
    
    def test_detect_ssh_brute_force(self):
        """Tester la détection d'une attaque par force brute SSH."""
        # Préparer les données de test
        log_entries = [
            "Failed password for root from 192.168.1.10 port 22 ssh2",
            "Failed password for root from 192.168.1.10 port 22 ssh2",
            "Failed password for root from 192.168.1.10 port 22 ssh2",
            "Failed password for root from 192.168.1.10 port 22 ssh2",
            "Failed password for root from 192.168.1.10 port 22 ssh2"
        ]
        
        # Exécuter la détection
        result = self.detector.analyze(log_entries)
        
        # Vérifier les résultats
        assert result["detected"] == True
        assert result["rule_name"] == "SSH Brute Force"
        assert result["severity"] == "high"
        assert result["matches"] == 5
        assert result["action"] == "redirect_to_lure"
    
    def test_no_detection(self):
        """Tester l'absence de détection."""
        # Préparer les données de test
        log_entries = [
            "Accepted password for admin from 192.168.1.10 port 22 ssh2",
            "User logged in successfully"
        ]
        
        # Exécuter la détection
        result = self.detector.analyze(log_entries)
        
        # Vérifier les résultats
        assert result["detected"] == False
    
    def test_detect_sql_injection(self):
        """Tester la détection d'une tentative d'injection SQL."""
        # Préparer les données de test
        log_entries = [
            "Request: SELECT * FROM users WHERE username='admin' OR 1=1"
        ]
        
        # Exécuter la détection
        result = self.detector.analyze(log_entries)
        
        # Vérifier les résultats
        assert result["detected"] == True
        assert result["rule_name"] == "SQL Injection Attempt"
        assert result["severity"] == "critical"
        assert result["action"] == "redirect_to_lure"


class TestDetectionEngine:
    """Tests pour le moteur de détection principal."""
    
    def setup_method(self):
        """Initialisation avant chaque test."""
        # Ces tests seront implémentés lorsque le code source du moteur de détection sera disponible
        pass
    
    def test_engine_initialization(self):
        """Tester l'initialisation du moteur de détection."""
        # À implémenter
        pass
    
    def test_combined_detection(self):
        """Tester la détection combinée (signature + anomalie + comportement)."""
        # À implémenter
        pass


if __name__ == "__main__":
    pytest.main(["-v", __file__])
