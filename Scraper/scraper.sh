#!/bin/bash

# Définir le PATH proprement
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Dossier du script = ./Scraper
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Fichier CSV dans le même dossier que le script
CSV_FILE="$SCRIPT_DIR/btc_prices.csv"

# URL de l'API OKX (bougie 1 min)
API_URL="https://www.okx.com/priapi/v5/market/candles?instId=BTC-USDT&limit=1&bar=1m"

# Vérifie si les outils sont là
for cmd in curl awk; do
    if ! command -v $cmd >/dev/null 2>&1; then
        echo "Erreur : '$cmd' requis mais introuvable."
        exit 1
    fi
done

# Récupérer les données de l'API
RESPONSE=$(curl -s "$API_URL")

if [[ -z "$RESPONSE" ]]; then
    echo "Erreur : aucune réponse de l'API."
    exit 1
fi

# Extraire le prix (5ᵉ élément = 'close')
PRICE=$(echo "$RESPONSE" | grep -oP '\[.*?\]' | head -1 | awk -F',' '{gsub(/"/, "", $5); print $5}')

# Timestamp
NOW=$(date +"%Y-%m-%d %H:%M:%S")

# Sauvegarder
if [[ -n "$PRICE" && "$PRICE" != "null" ]]; then
    echo "$NOW,$PRICE" >> "$CSV_FILE"
    echo "[OK] $NOW - Prix BTC : $PRICE USDT"
else
    echo "[ERREUR] Prix non récupéré."
fi
