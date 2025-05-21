#!/bin/bash

set -e  # Arrête le script si une commande échoue
set -x  # Affiche les commandes en cours (utile pour debug)

# Dossier courant
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Build des images
docker build --no-cache -t sdci_gateway "$DIR/gateway"       # Dockerfile pour les gateways
docker build --no-cache -t sdci_server_v1 "$DIR/server"        # Dockerfile pour le serveur
docker build --no-cache -t sdci_device "$DIR/device"           # Dockerfile pour l’application
# ... ajoute autant de lignes que nécessaire

echo -e "\n\033[0;32m✔️ Toutes les images ont été construites avec succès.\033[0m"
