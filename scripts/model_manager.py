#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de modèles pour GhostNet
-------------------------------------

Ce script permet d'exporter, d'importer, de mettre à jour et de valider
les modèles d'IA utilisés par GhostNet pour la détection des intrusions.
"""

import os
import sys
import json
import shutil
import pickle
import argparse
import datetime
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Définir les chemins
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
EXPORTS_DIR = BASE_DIR / "models" / "exported"


class ModelManager:
    """Gestionnaire de modèles pour les modèles d'IA GhostNet"""

    def __init__(self, verbose: bool = False):
        """
        Initialiser le gestionnaire de modèles
        
        Args:
            verbose: Activer le mode verbeux
        """
        self.verbose = verbose
        
        # Créer les répertoires s'ils n'existent pas
        MODELS_DIR.mkdir(exist_ok=True)
        EXPORTS_DIR.mkdir(exist_ok=True)

    def log(self, message: str) -> None:
        """
        Afficher un message en mode verbeux
        
        Args:
            message: Message à afficher
        """
        if self.verbose:
            print(f"[INFO] {message}")

    def error(self, message: str) -> None:
        """
        Afficher un message d'erreur
        
        Args:
            message: Message d'erreur à afficher
        """
        print(f"\033[91m[ERROR] {message}\033[0m")

    def success(self, message: str) -> None:
        """
        Afficher un message de succès
        
        Args:
            message: Message de succès à afficher
        """
        print(f"\033[92m[SUCCESS] {message}\033[0m")

    def get_model_path(self, model_name: str) -> Path:
        """
        Obtenir le chemin du modèle
        
        Args:
            model_name: Nom du modèle (ex: behavioral/network_traffic/traffic_classifier)
            
        Returns:
            Chemin vers le répertoire du modèle
        """
        return MODELS_DIR / model_name

    def get_model_file(self, model_name: str) -> Path:
        """
        Obtenir le chemin du fichier de modèle
        
        Args:
            model_name: Nom du modèle
            
        Returns:
            Chemin vers le fichier du modèle
        """
        model_path = self.get_model_path(model_name)
        
        # Rechercher les fichiers de modèle supportés
        extensions = [".pkl", ".h5", ".pt", ".onnx", ".pb"]
        for ext in extensions:
            model_file = model_path / f"model{ext}"
            if model_file.exists():
                return model_file
        
        # Si aucun fichier de modèle n'est trouvé, utiliser .pkl par défaut
        return model_path / "model.pkl"

    def get_metadata_file(self, model_name: str) -> Path:
        """
        Obtenir le chemin du fichier de métadonnées
        
        Args:
            model_name: Nom du modèle
            
        Returns:
            Chemin vers le fichier de métadonnées
        """
        return self.get_model_path(model_name) / "metadata.json"

    def model_exists(self, model_name: str) -> bool:
        """
        Vérifier si un modèle existe
        
        Args:
            model_name: Nom du modèle
            
        Returns:
            True si le modèle existe, False sinon
        """
        model_path = self.get_model_path(model_name)
        return model_path.exists()

    def load_metadata(self, model_name: str) -> Dict[str, Any]:
        """
        Charger les métadonnées d'un modèle
        
        Args:
            model_name: Nom du modèle
            
        Returns:
            Dictionnaire de métadonnées
        """
        metadata_file = self.get_metadata_file(model_name)
        
        if not metadata_file.exists():
            return {}
        
        with open(metadata_file, "r") as f:
            return json.load(f)

    def save_metadata(self, model_name: str, metadata: Dict[str, Any]) -> None:
        """
        Sauvegarder les métadonnées d'un modèle
        
        Args:
            model_name: Nom du modèle
            metadata: Dictionnaire de métadonnées
        """
        metadata_file = self.get_metadata_file(model_name)
        
        # Créer le répertoire parent si nécessaire
        metadata_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

    def export_model(self, model_name: str, output_file: Optional[str] = None) -> None:
        """
        Exporter un modèle vers un fichier
        
        Args:
            model_name: Nom du modèle
            output_file: Fichier de sortie (optionnel)
        """
        if not self.model_exists(model_name):
            self.error(f"Le modèle '{model_name}' n'existe pas")
            return
        
        model_path = self.get_model_path(model_name)
        metadata = self.load_metadata(model_name)
        
        # Créer un nom de fichier s'il n'est pas spécifié
        if output_file is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            output_file = EXPORTS_DIR / f"{model_name.replace('/', '_')}_{timestamp}.zip"
        else:
            output_file = Path(output_file)
        
        # Créer le répertoire parent si nécessaire
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Créer une archive contenant le modèle et ses métadonnées
        self.log(f"Exportation du modèle '{model_name}' vers '{output_file}'")
        
        try:
            # Nous utilisons shutil.make_archive pour créer une archive zip
            # Comme nous ne pouvons pas utiliser directement make_archive avec un Path,
            # nous utilisons str() pour convertir le chemin en chaîne
            output_base = str(output_file.with_suffix(""))
            shutil.make_archive(output_base, "zip", model_path)
            
            self.success(f"Modèle exporté avec succès vers '{output_file}'")
        except Exception as e:
            self.error(f"Erreur lors de l'exportation du modèle: {e}")

    def import_model(self, model_name: str, input_file: str) -> None:
        """
        Importer un modèle depuis un fichier
        
        Args:
            model_name: Nom du modèle
            input_file: Fichier d'entrée
        """
        input_path = Path(input_file)
        
        if not input_path.exists():
            self.error(f"Le fichier '{input_file}' n'existe pas")
            return
        
        model_path = self.get_model_path(model_name)
        
        # Sauvegarder le modèle existant si nécessaire
        if model_path.exists():
            self.log(f"Sauvegarde du modèle existant '{model_name}'")
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            backup_dir = EXPORTS_DIR / f"{model_name.replace('/', '_')}_{timestamp}_backup"
            
            # Copier le modèle existant vers le répertoire de sauvegarde
            shutil.copytree(model_path, backup_dir)
            self.log(f"Modèle sauvegardé dans '{backup_dir}'")
        
        # Créer le répertoire de destination
        model_path.mkdir(parents=True, exist_ok=True)
        
        # Extraire l'archive
        self.log(f"Importation du modèle depuis '{input_file}' vers '{model_name}'")
        
        try:
            # Extraire l'archive dans un répertoire temporaire
            temp_dir = Path(f"/tmp/ghostnet_import_{os.getpid()}")
            shutil.unpack_archive(input_file, extract_dir=temp_dir)
            
            # Copier les fichiers vers le répertoire de destination
            for item in temp_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, model_path)
                else:
                    shutil.copytree(item, model_path / item.name, dirs_exist_ok=True)
            
            # Nettoyer le répertoire temporaire
            shutil.rmtree(temp_dir)
            
            # Mettre à jour les métadonnées
            metadata = self.load_metadata(model_name)
            metadata["imported_at"] = datetime.datetime.now().isoformat()
            metadata["imported_from"] = input_file
            self.save_metadata(model_name, metadata)
            
            self.success(f"Modèle importé avec succès")
        except Exception as e:
            self.error(f"Erreur lors de l'importation du modèle: {e}")

    def update_metadata(self, model_name: str, metadata: Dict[str, Any]) -> None:
        """
        Mettre à jour les métadonnées d'un modèle
        
        Args:
            model_name: Nom du modèle
            metadata: Dictionnaire de métadonnées
        """
        if not self.model_exists(model_name):
            self.error(f"Le modèle '{model_name}' n'existe pas")
            return
        
        current_metadata = self.load_metadata(model_name)
        current_metadata.update(metadata)
        self.save_metadata(model_name, current_metadata)
        
        self.success(f"Métadonnées du modèle '{model_name}' mises à jour")

    def list_models(self) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Lister tous les modèles disponibles
        
        Returns:
            Liste de tuples (nom_modèle, métadonnées)
        """
        models = []
        
        for root, dirs, files in os.walk(MODELS_DIR):
            root_path = Path(root)
            
            # Vérifier si c'est un répertoire de modèle
            if "metadata.json" in files:
                # Calculer le chemin relatif par rapport au répertoire des modèles
                rel_path = root_path.relative_to(MODELS_DIR)
                model_name = str(rel_path)
                
                # Charger les métadonnées
                metadata = self.load_metadata(model_name)
                
                models.append((model_name, metadata))
        
        return models

    def display_models(self) -> None:
        """
        Afficher la liste des modèles disponibles
        """
        models = self.list_models()
        
        if not models:
            print("Aucun modèle trouvé")
            return
        
        print("\n=== Modèles disponibles ===\n")
        for model_name, metadata in models:
            print(f"- {model_name}")
            
            if "description" in metadata:
                print(f"  Description: {metadata['description']}")
            
            if "version" in metadata:
                print(f"  Version: {metadata['version']}")
            
            if "created_at" in metadata:
                print(f"  Créé le: {metadata['created_at']}")
            
            if "type" in metadata:
                print(f"  Type: {metadata['type']}")
            
            print("")

    def validate_model(self, model_name: str) -> bool:
        """
        Valider un modèle
        
        Args:
            model_name: Nom du modèle
            
        Returns:
            True si le modèle est valide, False sinon
        """
        if not self.model_exists(model_name):
            self.error(f"Le modèle '{model_name}' n'existe pas")
            return False
        
        metadata = self.load_metadata(model_name)
        model_file = self.get_model_file(model_name)
        
        # Vérifier si le fichier du modèle existe
        if not model_file.exists():
            self.error(f"Le fichier du modèle '{model_file}' n'existe pas")
            return False
        
        # Vérifier les métadonnées requises
        required_fields = ["type", "version"]
        missing_fields = [field for field in required_fields if field not in metadata]
        
        if missing_fields:
            self.error(f"Métadonnées manquantes: {', '.join(missing_fields)}")
            return False
        
        # Vérifier la cohérence du modèle
        try:
            # Pour les modèles pickle, tenter de les charger pour vérifier leur intégrité
            if model_file.suffix == ".pkl":
                with open(model_file, "rb") as f:
                    model = pickle.load(f)
                self.log(f"Modèle '{model_name}' chargé avec succès")
        except Exception as e:
            self.error(f"Erreur lors du chargement du modèle: {e}")
            return False
        
        self.success(f"Le modèle '{model_name}' est valide")
        return True

    def create_model(self, model_name: str, metadata: Dict[str, Any], model_data=None) -> None:
        """
        Créer un nouveau modèle
        
        Args:
            model_name: Nom du modèle
            metadata: Métadonnées du modèle
            model_data: Données du modèle (optionnel)
        """
        if self.model_exists(model_name):
            self.error(f"Le modèle '{model_name}' existe déjà")
            return
        
        model_path = self.get_model_path(model_name)
        model_file = self.get_model_file(model_name)
        
        # Créer le répertoire du modèle
        model_path.mkdir(parents=True, exist_ok=True)
        
        # Ajouter des métadonnées par défaut
        if "created_at" not in metadata:
            metadata["created_at"] = datetime.datetime.now().isoformat()
        
        if "version" not in metadata:
            metadata["version"] = "1.0.0"
        
        # Sauvegarder les métadonnées
        self.save_metadata(model_name, metadata)
        
        # Sauvegarder les données du modèle si fournies
        if model_data is not None:
            with open(model_file, "wb") as f:
                pickle.dump(model_data, f)
        
        self.success(f"Modèle '{model_name}' créé avec succès")


def main():
    """
    Point d'entrée principal du script
    """
    parser = argparse.ArgumentParser(description="Gestionnaire de modèles pour GhostNet")
    
    # Commandes principales
    subparsers = parser.add_subparsers(dest="command", help="Commande à exécuter")
    
    # Commande: list
    list_parser = subparsers.add_parser("list", help="Lister les modèles disponibles")
    
    # Commande: export
    export_parser = subparsers.add_parser("export", help="Exporter un modèle")
    export_parser.add_argument("--model", required=True, help="Nom du modèle à exporter")
    export_parser.add_argument("--output", help="Fichier de sortie (optionnel)")
    
    # Commande: import
    import_parser = subparsers.add_parser("import", help="Importer un modèle")
    import_parser.add_argument("--model", required=True, help="Nom du modèle à importer")
    import_parser.add_argument("--file", required=True, help="Fichier d'entrée")
    
    # Commande: update
    update_parser = subparsers.add_parser("update", help="Mettre à jour les métadonnées d'un modèle")
    update_parser.add_argument("--model", required=True, help="Nom du modèle à mettre à jour")
    update_parser.add_argument("--metadata", required=True, help="Fichier JSON contenant les métadonnées")
    
    # Commande: validate
    validate_parser = subparsers.add_parser("validate", help="Valider un modèle")
    validate_parser.add_argument("--model", required=True, help="Nom du modèle à valider")
    
    # Commande: create
    create_parser = subparsers.add_parser("create", help="Créer un nouveau modèle")
    create_parser.add_argument("--model", required=True, help="Nom du modèle à créer")
    create_parser.add_argument("--metadata", required=True, help="Fichier JSON contenant les métadonnées")
    create_parser.add_argument("--data", help="Fichier contenant les données du modèle (optionnel)")
    
    # Options globales
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode verbeux")
    
    # Analyser les arguments
    args = parser.parse_args()
    
    # Créer le gestionnaire de modèles
    manager = ModelManager(verbose=args.verbose)
    
    # Exécuter la commande appropriée
    if args.command == "list":
        manager.display_models()
    
    elif args.command == "export":
        manager.export_model(args.model, args.output)
    
    elif args.command == "import":
        manager.import_model(args.model, args.file)
    
    elif args.command == "update":
        # Charger les métadonnées depuis le fichier JSON
        try:
            with open(args.metadata, "r") as f:
                metadata = json.load(f)
        except Exception as e:
            manager.error(f"Erreur lors du chargement des métadonnées: {e}")
            return
        
        manager.update_metadata(args.model, metadata)
    
    elif args.command == "validate":
        manager.validate_model(args.model)
    
    elif args.command == "create":
        # Charger les métadonnées depuis le fichier JSON
        try:
            with open(args.metadata, "r") as f:
                metadata = json.load(f)
        except Exception as e:
            manager.error(f"Erreur lors du chargement des métadonnées: {e}")
            return
        
        # Charger les données du modèle si spécifiées
        model_data = None
        if args.data:
            try:
                with open(args.data, "rb") as f:
                    model_data = pickle.load(f)
            except Exception as e:
                manager.error(f"Erreur lors du chargement des données du modèle: {e}")
                return
        
        manager.create_model(args.model, metadata, model_data)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
