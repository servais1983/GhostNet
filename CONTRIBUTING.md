# Contribuer au projet GhostNet

Nous sommes très heureux que vous envisagiez de contribuer à GhostNet ! Ce document vous aidera à comprendre comment participer efficacement au projet.

## Table des matières

- [Code de conduite](#code-de-conduite)
- [Comment contribuer](#comment-contribuer)
  - [Signaler des bugs](#signaler-des-bugs)
  - [Suggérer des améliorations](#suggérer-des-améliorations)
  - [Contribuer au code](#contribuer-au-code)
  - [Documentation](#documentation)
- [Normes de codage](#normes-de-codage)
- [Processus de pull request](#processus-de-pull-request)
- [Environnement de développement](#environnement-de-développement)
- [Tests](#tests)
- [Structure du projet](#structure-du-projet)

## Code de conduite

Ce projet adhère à un code de conduite qui attend de tous les participants qu'ils se respectent mutuellement. Veuillez lire le [CODE_DE_CONDUITE.md](CODE_OF_CONDUCT.md) avant de participer.

## Comment contribuer

### Signaler des bugs

Les bugs sont suivis via les issues GitHub. Lorsque vous signalez un bug, veuillez inclure :

- Un titre clair et descriptif
- Les étapes précises pour reproduire le problème
- Le comportement attendu et le comportement observé
- Des captures d'écran si nécessaire
- Informations sur votre environnement (OS, version de Python, etc.)

### Suggérer des améliorations

Les suggestions d'amélioration sont également gérées via les issues GitHub. Incluez :

- Un titre clair et descriptif
- Une description détaillée de l'amélioration proposée
- Les bénéfices attendus de cette amélioration
- Des exemples concrets d'utilisation si possible

### Contribuer au code

1. **Fork** le dépôt sur GitHub
2. **Clone** votre fork localement
3. **Créez une branche** pour vos modifications
4. **Faites vos modifications** et commit avec des messages explicites
5. **Testez** vos modifications
6. **Push** votre branche sur votre fork
7. **Soumettez une pull request** vers la branche principale du projet

### Documentation

La documentation est aussi importante que le code lui-même. Vous pouvez améliorer :

- Les guides d'utilisation et d'installation
- Les exemples de code et de configuration
- Les commentaires dans le code
- Les diagrammes d'architecture et schémas explicatifs

## Normes de codage

Pour maintenir la qualité et la lisibilité du code, veuillez suivre ces directives :

### Style de code Python

- Suivez la norme [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Utilisez des noms de variables et de fonctions explicites
- Commentez votre code de manière appropriée
- Ajoutez des docstrings pour toutes les classes et fonctions

### Formatage du code

Avant de soumettre une pull request, assurez-vous que votre code est formaté correctement :

```bash
# Installation des outils de formatage
pip install black flake8 isort mypy

# Formatage du code
black ghostnet/
isort ghostnet/
flake8 ghostnet/
mypy ghostnet/
```

## Processus de pull request

1. Assurez-vous que votre code respecte les normes de codage
2. Mettez à jour la documentation si nécessaire
3. Ajoutez ou mettez à jour les tests pour refléter vos modifications
4. Assurez-vous que tous les tests passent
5. Soumettez votre pull request avec une description claire de vos modifications

Un mainteneur du projet examinera votre pull request et pourra suggérer des modifications ou des améliorations avant de la fusionner.

## Environnement de développement

Pour configurer votre environnement de développement :

```bash
# Cloner le dépôt
git clone https://github.com/votre-username/GhostNet.git
cd GhostNet

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances de développement
pip install -e ".[dev]"
```

## Tests

Les tests sont essentiels pour maintenir la qualité du code. Pour exécuter les tests :

```bash
# Exécuter tous les tests
pytest

# Exécuter les tests avec couverture de code
pytest --cov=ghostnet tests/
```

Pour ajouter de nouveaux tests, créez des fichiers dans le répertoire `tests/` qui suivent les conventions de nommage existantes.

## Structure du projet

Voici la structure générale du projet pour vous aider à comprendre où placer vos contributions :

```
GhostNet/
├── config/                # Fichiers de configuration
├── docs/                  # Documentation
├── ghostnet/              # Code source principal
│   ├── ai_engine/         # Moteur d'intelligence artificielle
│   ├── api/               # API REST
│   ├── detection/         # Système de détection
│   ├── lure_generator/    # Générateur de leurres
│   ├── network_manager/   # Gestionnaire de réseau
│   ├── utils/             # Utilitaires
│   └── ...
├── models/                # Modèles d'IA
├── scripts/               # Scripts utilitaires
├── tests/                 # Tests
└── ...
```

---

Merci de contribuer à GhostNet ! Votre aide est précieuse pour améliorer ce projet et renforcer la sécurité des systèmes informatiques.
