#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GhostNet - Une solution de cybersécurité basée sur la déception et l'IA
pour la détection et l'analyse des intrusions.

GhostNet crée un double virtuel de votre réseau, interconnecté au système réel
mais isolé physiquement. Ce double mime le comportement du réseau réel,
s'adapte en temps réel aux techniques d'attaque et piège les attaquants
dans un environnement fictif.
"""

__version__ = "1.0.0"
__author__ = "GhostNet Team"
__email__ = "contact@ghostnet-security.com"
__license__ = "MIT"
__copyright__ = "Copyright 2025 GhostNet Security"

# Importer les modules principaux pour les exposer au niveau du package
from . import api
# Les autres modules seront importés ici au fur et à mesure de leur création
