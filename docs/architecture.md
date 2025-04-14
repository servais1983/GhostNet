# Architecture de GhostNet

Ce document présente l'architecture globale du système GhostNet, ses principaux composants et leurs interactions.

## Vue d'ensemble

GhostNet est une plateforme de sécurité basée sur la déception qui utilise l'intelligence artificielle pour créer dynamiquement des leurres adaptés aux menaces détectées. L'architecture a été conçue pour être modulaire, évolutive et facilement adaptable à différents environnements.

![Architecture GhostNet](assets/architecture_diagram.png)

## Composants principaux

### 1. Moteur de détection (Detection Engine)

Le moteur de détection est responsable de l'identification des tentatives d'intrusion et des comportements malveillants. Il utilise trois méthodes complémentaires :

- **Détection par signature** : Identifie les attaques connues à partir de modèles prédéfinis
- **Détection par anomalie** : Détecte les écarts par rapport au comportement normal du réseau
- **Détection comportementale** : Analyse les séquences d'actions pour identifier les intentions malveillantes

Ce moteur est le premier point de contact avec le trafic entrant et détermine si une communication doit être dirigée vers un leurre.

### 2. Générateur de leurres (Lure Generator)

Le générateur de leurres crée et maintient des environnements fictifs conçus pour tromper les attaquants. Ses fonctionnalités principales sont :

- Création de services simulés (SSH, HTTP, SMTP, etc.)
- Génération de données fictives mais réalistes
- Adaptation dynamique du comportement des leurres en fonction des actions de l'attaquant
- Virtualisation légère pour isoler les environnements leurres

Le générateur utilise des modèles IA pour garantir le réalisme des leurres et leur capacité à maintenir l'intérêt des attaquants sophistiqués.

### 3. Gestionnaire de réseau (Network Manager)

Le gestionnaire de réseau contrôle le flux de données entre le réseau réel et les environnements leurres. Il est responsable de :

- La redirection transparente du trafic malveillant vers les leurres
- L'isolation entre le réseau de production et les environnements de leurre
- La limitation du trafic sortant depuis les leurres pour prévenir les rebonds d'attaque
- La virtualisation des interfaces réseau et la gestion des espaces de noms

Ce composant garantit que les attaquants ne peuvent pas s'échapper des leurres vers le réseau réel.

### 4. Moteur d'intelligence artificielle (AI Engine)

Le cœur intelligent de GhostNet, ce moteur utilise plusieurs techniques d'IA pour :

- Analyser le comportement des attaquants
- Prédire leurs prochaines actions
- Adapter les leurres en temps réel
- Identifier les nouvelles techniques d'attaque
- Générer des rapports de renseignement sur les menaces

Le moteur d'IA s'appuie sur des modèles pré-entraînés qui sont continuellement affinés à partir des interactions avec les attaquants.

### 5. API REST

L'API REST fournit une interface programmatique pour interagir avec GhostNet :

- Gestion des leurres (création, modification, suppression)
- Récupération des alertes et des rapports
- Configuration du système
- Intégration avec d'autres outils de sécurité

L'API est sécurisée par authentification et peut être utilisée pour construire des interfaces personnalisées ou intégrer GhostNet dans des workflows existants.

### 6. Module d'intégration (Integration Module)

Ce module permet à GhostNet de communiquer avec des systèmes externes :

- SIEM (Security Information and Event Management)
- Plateformes de threat intelligence
- Outils d'orchestration de sécurité
- Systèmes de notification

Les intégrations prédéfinies incluent Elasticsearch, Splunk et les serveurs Syslog, avec la possibilité de créer des connecteurs personnalisés.

## Flux de données

1. Le trafic réseau est analysé par le moteur de détection
2. Si une activité suspecte est détectée, le gestionnaire de réseau redirige la connexion vers un leurre approprié
3. Le générateur de leurres construit ou adapte un environnement qui répond aux attentes de l'attaquant
4. L'attaquant interagit avec le leurre, croyant être dans un système réel
5. Le moteur d'IA analyse les actions de l'attaquant et ajuste le comportement du leurre
6. Les informations sur l'attaque sont collectées et envoyées aux systèmes de monitoring et d'alerte
7. Les connaissances acquises sont utilisées pour améliorer la détection future

## Isolation et sécurité

GhostNet utilise plusieurs mécanismes pour garantir que les attaquants ne peuvent pas s'échapper des environnements leurres :

- **Namespaces réseau** : Isolation au niveau du système d'exploitation
- **Conteneurisation** : Isolation des processus et des ressources
- **Filtrage du trafic sortant** : Limitation stricte des connexions initiées depuis les leurres
- **Surveillance continue** : Détection des tentatives d'évasion ou de pivotement

## Extensibilité

L'architecture modulaire de GhostNet permet d'ajouter facilement de nouvelles fonctionnalités :

- Nouveaux types de leurres
- Algorithmes de détection supplémentaires
- Intégrations avec d'autres systèmes
- Modules d'analyse personnalisés

Chaque composant expose des interfaces bien définies qui peuvent être étendues ou remplacées selon les besoins.

## Déploiement

GhostNet peut être déployé dans diverses configurations :

- **Standalone** : Installation sur un serveur dédié avec deux interfaces réseau
- **Distribué** : Composants répartis sur plusieurs serveurs pour une meilleure évolutivité
- **Cloud** : Déploiement dans des environnements cloud avec des adaptations pour la virtualisation réseau
- **Hybride** : Combinaison de déploiements sur site et dans le cloud

Le déploiement minimal recommandé inclut une machine avec deux interfaces réseau : une pour la gestion et une pour les honeypots.
