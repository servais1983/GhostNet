#!/bin/bash
# Script d'installation de GhostNet
# Ce script installe toutes les dépendances nécessaires et configure l'environnement

set -e

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logo
echo -e "${BLUE}"
echo "  ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗███╗   ██╗███████╗████████╗"
echo " ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝████╗  ██║██╔════╝╚══██╔══╝"
echo " ██║  ███╗███████║██║   ██║███████╗   ██║   ██╔██╗ ██║█████╗     ██║   "
echo " ██║   ██║██╔══██║██║   ██║╚════██║   ██║   ██║╚██╗██║██╔══╝     ██║   "
echo " ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ██║ ╚████║███████╗   ██║   "
echo "  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═══╝╚══════╝   ╚═╝   "
echo -e "${NC}"
echo -e "${GREEN}Script d'installation de GhostNet${NC}"
echo -e "${YELLOW}---------------------------------------${NC}"

# Vérifier si l'utilisateur est root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Ce script doit être exécuté en tant que root${NC}"
  echo -e "${YELLOW}Utilisez: sudo $0${NC}"
  exit 1
fi

# Fonction pour vérifier les dépendances système
check_dependencies() {
  echo -e "${BLUE}[*] Vérification des dépendances système...${NC}"
  
  DEPENDENCIES=("python3" "python3-pip" "python3-venv" "iptables" "net-tools" "tcpdump" "curl" "git")
  MISSING=()

  for dep in "${DEPENDENCIES[@]}"; do
    if ! command -v $dep &> /dev/null && ! dpkg -l | grep -q $dep; then
      MISSING+=("$dep")
    fi
  done

  if [ ${#MISSING[@]} -gt 0 ]; then
    echo -e "${YELLOW}[!] Dépendances manquantes: ${MISSING[*]}${NC}"
    echo -e "${GREEN}[+] Installation des dépendances manquantes...${NC}"
    apt update
    apt install -y ${MISSING[@]}
  else
    echo -e "${GREEN}[+] Toutes les dépendances système sont installées.${NC}"
  fi
}

# Fonction pour créer l'environnement virtuel Python
create_venv() {
  echo -e "${BLUE}[*] Création de l'environnement virtuel Python...${NC}"
  
  if [ -d "venv" ]; then
    echo -e "${YELLOW}[!] L'environnement virtuel existe déjà.${NC}"
    read -p "Voulez-vous le recréer? (o/N) " choice
    case "$choice" in 
      o|O )
        echo -e "${YELLOW}[!] Suppression de l'environnement virtuel existant...${NC}"
        rm -rf venv
        ;;
      * )
        echo -e "${GREEN}[+] Utilisation de l'environnement virtuel existant.${NC}"
        return
        ;;
    esac
  fi
  
  python3 -m venv venv
  echo -e "${GREEN}[+] Environnement virtuel créé avec succès.${NC}"
}

# Installer les dépendances Python
install_python_dependencies() {
  echo -e "${BLUE}[*] Installation des dépendances Python...${NC}"
  
  # Activer l'environnement virtuel
  source venv/bin/activate
  
  # Installer les dépendances
  pip install --upgrade pip
  pip install -r requirements.txt
  
  echo -e "${GREEN}[+] Dépendances Python installées avec succès.${NC}"
}

# Configurer les permissions des fichiers
set_permissions() {
  echo -e "${BLUE}[*] Configuration des permissions...${NC}"
  
  # Rendre les scripts exécutables
  chmod +x scripts/*.sh
  chmod +x ghostnet/*.py
  
  # Créer les répertoires nécessaires s'ils n'existent pas
  mkdir -p logs data config/certs
  
  # Définir les permissions
  chmod 750 logs data config/certs
  
  echo -e "${GREEN}[+] Permissions configurées avec succès.${NC}"
}

# Télécharger les modèles d'IA pré-entraînés
download_models() {
  echo -e "${BLUE}[*] Téléchargement des modèles d'IA...${NC}"
  
  # Créer le répertoire des modèles
  mkdir -p models/nlp/command_classifier
  mkdir -p models/nlp/intent_recognizer
  mkdir -p models/behavioral/network_traffic
  mkdir -p models/anomaly/flow_analysis
  
  # Télécharger les modèles (simulation)
  echo -e "${YELLOW}[!] Cette étape est une simulation. Dans une version de production, les modèles seraient téléchargés depuis un serveur distant.${NC}"
  touch models/nlp/command_classifier/model.pkl
  touch models/nlp/intent_recognizer/model.pkl
  touch models/behavioral/network_traffic/model.pkl
  touch models/anomaly/flow_analysis/model.pkl
  
  echo -e "${GREEN}[+] Modèles d'IA téléchargés avec succès.${NC}"
}

# Générer les certificats SSL pour l'API
generate_ssl_certs() {
  echo -e "${BLUE}[*] Génération des certificats SSL pour l'API...${NC}"
  
  if [ -f "config/certs/server.crt" ] && [ -f "config/certs/server.key" ]; then
    echo -e "${YELLOW}[!] Les certificats SSL existent déjà.${NC}"
    read -p "Voulez-vous les régénérer? (o/N) " choice
    case "$choice" in 
      o|O )
        echo -e "${YELLOW}[!] Régénération des certificats SSL...${NC}"
        ;;
      * )
        echo -e "${GREEN}[+] Utilisation des certificats SSL existants.${NC}"
        return
        ;;
    esac
  fi
  
  # Générer un certificat auto-signé
  openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout config/certs/server.key -out config/certs/server.crt \
    -subj "/C=FR/ST=Paris/L=Paris/O=GhostNet/OU=Security/CN=localhost"
  
  echo -e "${GREEN}[+] Certificats SSL générés avec succès.${NC}"
}

# Configuration des règles de pare-feu
configure_firewall() {
  echo -e "${BLUE}[*] Configuration des règles de pare-feu...${NC}"
  
  # Sauvegarder les règles actuelles
  iptables-save > config/iptables.backup
  
  echo -e "${YELLOW}[!] Cette étape est désactivée dans le script d'installation.${NC}"
  echo -e "${YELLOW}[!] Dans une version de production, les règles de pare-feu seraient configurées automatiquement.${NC}"
  echo -e "${YELLOW}[!] Pour configurer manuellement les règles, utilisez le script scripts/setup_firewall.sh${NC}"
  
  echo -e "${GREEN}[+] Configuration du pare-feu terminée.${NC}"
}

# Installation principale
main() {
  check_dependencies
  create_venv
  install_python_dependencies
  set_permissions
  download_models
  generate_ssl_certs
  configure_firewall
  
  echo -e "${GREEN}[+] Installation de GhostNet terminée avec succès!${NC}"
  echo -e "${BLUE}[*] Pour démarrer GhostNet, exécutez:${NC}"
  echo -e "${YELLOW}   $ source venv/bin/activate${NC}"
  echo -e "${YELLOW}   $ python ghostnet/server.py --config=config/config.yaml${NC}"
}

# Exécuter l'installation
main
