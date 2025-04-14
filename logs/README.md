# Journaux d'événements GhostNet

Ce répertoire contient les fichiers de journalisation générés par GhostNet. Ces journaux sont essentiels pour le suivi des activités, le débogage et l'analyse forensique.

## Structure des fichiers de journalisation

- `ghostnet.log` - Journal principal du système
- `api.log` - Journal de l'API REST
- `detection.log` - Journal du module de détection
- `lure.log` - Journal du générateur de leurres
- `network.log` - Journal du gestionnaire de réseau
- `ai.log` - Journal du moteur d'IA

## Niveaux de journalisation

GhostNet utilise les niveaux de journalisation standard suivants :

- `DEBUG` - Informations détaillées pour le débogage
- `INFO` - Informations générales sur le fonctionnement normal
- `WARNING` - Avertissements qui n'empêchent pas le fonctionnement
- `ERROR` - Erreurs qui empêchent certaines fonctionnalités
- `CRITICAL` - Erreurs critiques qui empêchent le fonctionnement principal

## Format des journaux

Chaque entrée de journal suit le format suivant :

```
[TIMESTAMP] [LEVEL] [MODULE] [MESSAGE]
```

Exemple :
```
[2025-04-14 12:34:56] [INFO] [DetectionEngine] Nouvelle tentative de connexion détectée depuis 192.168.1.100
```

## Rotation des journaux

Les fichiers de journalisation font l'objet d'une rotation automatique pour éviter une croissance excessive :

- Rotation quotidienne à minuit
- Compression des anciens journaux
- Conservation des 30 derniers jours

## Alertes et notifications

Les événements critiques et les erreurs sont automatiquement envoyés au système d'alerte configuré dans `config/config.yaml`.

## Confidentialité et sécurité

Les journaux peuvent contenir des informations sensibles. Assurez-vous de :

- Limiter l'accès à ce répertoire
- Anonymiser les journaux avant de les partager
- Chiffrer les sauvegardes des journaux

## Analyse des journaux

Pour analyser les journaux, utilisez les scripts fournis dans le répertoire `scripts/` :

```bash
# Rechercher des modèles d'attaque spécifiques
python scripts/log_analyzer.py --pattern="SSH brute force" --log=logs/detection.log

# Générer un rapport d'activité
python scripts/log_analyzer.py --report --period=daily --output=reports/daily_activity.pdf
```

## Remarque importante

Ne supprimez pas manuellement les fichiers de ce répertoire pendant que GhostNet est en cours d'exécution. Pour effacer les journaux, utilisez la commande :

```bash
python scripts/maintenance.py --clear-logs
```
