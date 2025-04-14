# Modèles d'IA pour GhostNet

Ce répertoire contient les modèles d'intelligence artificielle utilisés par GhostNet pour la détection des intrusions et l'analyse comportementale.

## Structure des modèles

- `nlp/` : Modèles de traitement du langage naturel
  - `command_classifier/` : Modèle pour classifier les commandes malveillantes
  - `intent_recognizer/` : Modèle pour détecter l'intention des utilisateurs

- `behavioral/` : Modèles d'analyse comportementale
  - `network_traffic/` : Modèles pour l'analyse du trafic réseau
  - `user_activity/` : Modèles pour l'analyse du comportement des utilisateurs

- `anomaly/` : Modèles de détection d'anomalies
  - `flow_analysis/` : Modèles pour analyser les flux de données
  - `time_series/` : Modèles pour analyser les séries temporelles

## Exportation et importation des modèles

Les modèles peuvent être exportés et importés à l'aide des scripts situés dans le répertoire `scripts/`:

```bash
# Exporter un modèle
python scripts/model_manager.py export --model behavioral/network_traffic/traffic_classifier

# Importer un modèle
python scripts/model_manager.py import --model behavioral/network_traffic/traffic_classifier --file models/exported/traffic_classifier_v2.pkl
```

## Format des modèles

GhostNet prend en charge plusieurs types de modèles :

- Modèles scikit-learn (format .pkl)
- Modèles TensorFlow/Keras (format .h5 ou SavedModel)
- Modèles PyTorch (format .pt)

Pour ajouter un nouveau modèle, assurez-vous de respecter la structure de dossiers et d'inclure un fichier `metadata.json` décrivant le modèle.

## Entraînement des modèles

Pour réentraîner un modèle existant, utilisez le script d'entraînement :

```bash
python scripts/train_model.py --model behavioral/network_traffic/traffic_classifier --data data/training/traffic_data.csv
```

## Modèles par défaut

Lors de la première installation, GhostNet téléchargera automatiquement les modèles par défaut depuis le dépôt distant. Si vous souhaitez utiliser vos propres modèles, vous pouvez les placer dans les répertoires correspondants.
