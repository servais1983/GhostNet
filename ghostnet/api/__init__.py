#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module d'API pour GhostNet.

Ce package fournit une interface REST pour interagir avec le système GhostNet,
permettant de contrôler les honeypots, récupérer les données de détection
et gérer la configuration.
"""

from .app import app, api, main
