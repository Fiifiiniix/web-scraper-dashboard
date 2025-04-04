#!/bin/bash

cd /home/fiifiiniix/web-scraper-dashboard

# Vérifie s'il y a eu une modification du fichier avant de commit
if git diff --quiet Scraper/btc_prices.csv; then
    echo "[$(date)] Aucune modification à pousser."
else
    git add Scraper/btc_prices.csv
    git commit -m "Mise à jour automatique du CSV à $(date '+%Y-%m-%d %H:%M')"
    git push
    echo "[$(date)] Fichier CSV poussé sur GitHub."
fi
