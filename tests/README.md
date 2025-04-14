# Tests pour GhostNet

Ce répertoire contient l'ensemble des tests pour le projet GhostNet. Ces tests permettent de valider le bon fonctionnement des différents modules et de s'assurer que les nouvelles fonctionnalités n'introduisent pas de régressions.

## Structure des tests

- `unit/` - Tests unitaires pour chaque module
- `integration/` - Tests d'intégration entre les différents modules
- `functional/` - Tests fonctionnels des cas d'utilisation principaux
- `performance/` - Tests de performance et de charge
- `security/` - Tests de sécurité et de vulnérabilité

## Exécution des tests

Pour exécuter tous les tests :

```bash
# S'assurer d'être dans l'environnement virtuel
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Exécuter tous les tests
pytest

# Exécuter les tests avec couverture de code
pytest --cov=ghostnet tests/

# Générer un rapport de couverture HTML
pytest --cov=ghostnet --cov-report=html tests/
```

## Tests spécifiques

Pour exécuter un groupe spécifique de tests :

```bash
# Tests unitaires seulement
pytest tests/unit/

# Tests pour un module spécifique
pytest tests/unit/test_detection.py

# Tests pour une classe spécifique
pytest tests/unit/test_detection.py::TestSignatureDetector

# Tests pour une méthode spécifique
pytest tests/unit/test_detection.py::TestSignatureDetector::test_detect_ssh_brute_force
```

## Écriture de nouveaux tests

Lorsque vous ajoutez de nouvelles fonctionnalités, assurez-vous d'inclure les tests correspondants. Suivez ces principes :

1. **Tests unitaires** : Testez chaque fonction ou méthode individuellement
2. **Tests d'intégration** : Testez l'interaction entre plusieurs modules
3. **Tests fonctionnels** : Testez des scénarios complets d'utilisation
4. **Utilisation de mocks** : Utilisez des mocks pour simuler les dépendances externes

### Exemple de test unitaire

```python
# tests/unit/test_detection.py
import pytest
from ghostnet.detection import SignatureDetector

class TestSignatureDetector:
    def setup_method(self):
        self.detector = SignatureDetector()
        
    def test_detect_ssh_brute_force(self):
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
```

## Fixtures de test

Des fixtures communes sont disponibles dans `tests/conftest.py` pour faciliter la configuration des tests. Par exemple :

```python
# tests/conftest.py
import pytest
import yaml
from pathlib import Path

@pytest.fixture
def config():
    """Charger la configuration de test."""
    config_path = Path(__file__).parent / "data" / "test_config.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

@pytest.fixture
def mock_network():
    """Créer un mock du gestionnaire de réseau."""
    # Configuration du mock
    # ...
    return mock
```

## Données de test

Le répertoire `tests/data/` contient les fichiers de données utilisés dans les tests :

- `test_config.yaml` - Configuration pour les tests
- `sample_logs/` - Exemples de fichiers journaux pour tester la détection
- `network_captures/` - Captures réseau pour les tests d'intégration

## Tests de régression

Pour éviter les régressions, nous comparons les résultats des tests avec des résultats de référence stockés dans `tests/references/`.

## Intégration continue

Les tests sont automatiquement exécutés lors des pull requests via notre système d'intégration continue. Une pull request ne peut être fusionnée que si tous les tests passent.

---

N'hésitez pas à contacter l'équipe si vous avez des questions sur l'écriture ou l'exécution des tests.
