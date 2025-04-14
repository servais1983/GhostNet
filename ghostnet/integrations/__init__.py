#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module d'intégration pour GhostNet.

Ce package fournit des intégrations avec divers systèmes externes,
tels que les SIEM, les plateformes de threat intelligence, etc.
"""

from .siem import SIEMIntegration, ElasticSIEM, SplunkSIEM, SyslogSIEM, create_siem_integration
