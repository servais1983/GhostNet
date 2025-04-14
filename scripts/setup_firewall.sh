#!/bin/bash
# Script de configuration du pare-feu pour GhostNet
# Ce script configure les règles iptables nécessaires pour le fonctionnement du honeypot

set -e

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
HONEYPOT_INTERFACE="eth1"  # Interface réseau dédiée au honeypot
MANAGEMENT_INTERFACE="eth0"  # Interface réseau de gestion
CONFIG_FILE="config/config.yaml"
PORTS=(22 23 80 443 8080 3306 3389 445 1883 502)  # Ports par défaut à rediriger

# Vérifier si l'utilisateur est root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Ce script doit être exécuté en tant que root${NC}"
  echo -e "${YELLOW}Utilisez: sudo $0${NC}"
  exit 1
fi

# Fonction pour afficher l'aide
show_help() {
  echo -e "${BLUE}Configuration du pare-feu pour GhostNet${NC}"
  echo -e "${YELLOW}---------------------------------------${NC}"
  echo -e "Usage: $0 [OPTIONS]"
  echo -e ""
  echo -e "Options:"
  echo -e "  -h, --help              Afficher cette aide"
  echo -e "  -c, --config FILE       Spécifier un fichier de configuration (défaut: ${CONFIG_FILE})"
  echo -e "  -m, --management IF     Spécifier l'interface de gestion (défaut: ${MANAGEMENT_INTERFACE})"
  echo -e "  -n, --honeypot IF       Spécifier l'interface honeypot (défaut: ${HONEYPOT_INTERFACE})"
  echo -e "  -p, --ports PORTS       Liste des ports à rediriger, séparés par des virgules"
  echo -e "  -s, --save              Sauvegarder les règles iptables"
  echo -e "  -r, --restore           Restaurer les règles iptables précédentes"
}

# Fonction pour valider le fichier de configuration
validate_config() {
  if [ ! -f "$1" ]; then
    echo -e "${RED}[!] Erreur: Fichier de configuration introuvable: $1${NC}"
    exit 1
  fi
}

# Fonction pour valider l'interface réseau
validate_interface() {
  if ! ip link show "$1" &> /dev/null; then
    echo -e "${RED}[!] Erreur: Interface réseau introuvable: $1${NC}"
    exit 1
  fi
}

# Fonction pour sauvegarder les règles iptables actuelles
backup_iptables() {
  echo -e "${BLUE}[*] Sauvegarde des règles iptables actuelles...${NC}"
  
  if [ -f "config/iptables.backup" ]; then
    # Créer une sauvegarde datée si une sauvegarde existe déjà
    BACKUP_FILE="config/iptables.backup.$(date +%Y%m%d-%H%M%S)"
    cp config/iptables.backup "$BACKUP_FILE"
    echo -e "${YELLOW}[!] Sauvegarde précédente déplacée vers $BACKUP_FILE${NC}"
  fi
  
  iptables-save > config/iptables.backup
  echo -e "${GREEN}[+] Règles iptables sauvegardées dans config/iptables.backup${NC}"
}

# Fonction pour restaurer les règles iptables
restore_iptables() {
  echo -e "${BLUE}[*] Restauration des règles iptables précédentes...${NC}"
  
  if [ ! -f "config/iptables.backup" ]; then
    echo -e "${RED}[!] Erreur: Fichier de sauvegarde iptables introuvable${NC}"
    exit 1
  fi
  
  iptables-restore < config/iptables.backup
  echo -e "${GREEN}[+] Règles iptables restaurées avec succès${NC}"
}

# Fonction pour configurer le NAT et les redirections
setup_nat_and_redirections() {
  echo -e "${BLUE}[*] Configuration du NAT et des redirections...${NC}"
  
  # Activer le forwarding IP
  echo 1 > /proc/sys/net/ipv4/ip_forward
  
  # Nettoyer les règles existantes liées au honeypot
  iptables -t nat -F PREROUTING
  iptables -F FORWARD
  
  # Créer une chaîne spécifique pour GhostNet
  iptables -N GHOSTNET 2>/dev/null || iptables -F GHOSTNET
  
  # Configuration du NAT pour les redirections
  for port in "${PORTS[@]}"; do
    echo -e "${YELLOW}[!] Configuration de la redirection pour le port $port...${NC}"
    
    # Rediriger le trafic entrant sur l'interface honeypot vers le service leurre
    iptables -t nat -A PREROUTING -i $HONEYPOT_INTERFACE -p tcp --dport $port -j REDIRECT --to-port $port
    
    # Permettre le trafic entrant vers le service leurre
    iptables -A INPUT -i $HONEYPOT_INTERFACE -p tcp --dport $port -j ACCEPT
    
    # Ajouter une règle dans la chaîne GHOSTNET pour la journalisation
    iptables -A GHOSTNET -p tcp --dport $port -j LOG --log-prefix "GHOSTNET-CONN: " --log-level 4
  done
  
  # Isolation du honeypot : interdire tout trafic sortant non nécessaire
  iptables -A FORWARD -i $HONEYPOT_INTERFACE -o $MANAGEMENT_INTERFACE -j DROP
  iptables -A FORWARD -i $MANAGEMENT_INTERFACE -o $HONEYPOT_INTERFACE -j DROP
  
  # Permettre au trafic de gestion d'accéder au honeypot via l'API
  iptables -A INPUT -i $MANAGEMENT_INTERFACE -p tcp --dport 8080 -j ACCEPT
  iptables -A INPUT -i $MANAGEMENT_INTERFACE -p tcp --dport 8443 -j ACCEPT
  
  echo -e "${GREEN}[+] NAT et redirections configurés avec succès${NC}"
}

# Fonction pour configurer la limitation de débit
setup_rate_limiting() {
  echo -e "${BLUE}[*] Configuration de la limitation de débit...${NC}"
  
  # Limiter les connexions HTTP/HTTPS
  iptables -A INPUT -p tcp --dport 80 -m state --state NEW -m limit --limit 20/minute --limit-burst 10 -j ACCEPT
  iptables -A INPUT -p tcp --dport 443 -m state --state NEW -m limit --limit 20/minute --limit-burst 10 -j ACCEPT
  
  # Limiter les tentatives de connexion SSH
  iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m limit --limit 5/minute --limit-burst 3 -j ACCEPT
  
  echo -e "${GREEN}[+] Limitation de débit configurée avec succès${NC}"
}

# Configuration principale
main() {
  # Traiter les arguments
  while [[ "$#" -gt 0 ]]; do
    case $1 in
      -h|--help)
        show_help
        exit 0
        ;;
      -c|--config)
        CONFIG_FILE="$2"
        shift
        ;;
      -m|--management)
        MANAGEMENT_INTERFACE="$2"
        shift
        ;;
      -n|--honeypot)
        HONEYPOT_INTERFACE="$2"
        shift
        ;;
      -p|--ports)
        IFS=',' read -ra PORTS <<< "$2"
        shift
        ;;
      -s|--save)
        backup_iptables
        exit 0
        ;;
      -r|--restore)
        restore_iptables
        exit 0
        ;;
      *)
        echo -e "${RED}[!] Option inconnue: $1${NC}"
        show_help
        exit 1
        ;;
    esac
    shift
  done
  
  # Valider les entrées
  validate_config "$CONFIG_FILE"
  validate_interface "$MANAGEMENT_INTERFACE"
  validate_interface "$HONEYPOT_INTERFACE"
  
  # Sauvegarder les règles actuelles
  backup_iptables
  
  # Configurer le pare-feu
  setup_nat_and_redirections
  setup_rate_limiting
  
  echo -e "${GREEN}[+] Configuration du pare-feu terminée avec succès!${NC}"
  echo -e "${YELLOW}[!] Pour rendre ces règles persistantes après redémarrage, utilisez:${NC}"
  echo -e "${YELLOW}   $ sudo iptables-save > /etc/iptables/rules.v4${NC}"
}

# Exécuter la configuration
main "$@"
