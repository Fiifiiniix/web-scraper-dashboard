import pandas as pd
import os
import json
from datetime import datetime

# Lire les données CSV
csv_path = "../Scraper/btc_prices.csv"
df = pd.read_csv(csv_path, names=["datetime", "price"])
df["datetime"] = pd.to_datetime(df["datetime"])
df["price"] = pd.to_numeric(df["price"], errors='coerce')

# Filtrer les données du jour
today = datetime.now().strftime("%Y-%m-%d")
df_today = df[df["datetime"].dt.strftime("%Y-%m-%d") == today]

if df_today.empty:
    print("Aucune donnée pour aujourd'hui.")
    exit()

# Calculs
open_price = df_today.iloc[0]["price"]
close_price = df_today.iloc[-1]["price"]
change_pct = ((close_price - open_price) / open_price) * 100
volatility = df_today["price"].std()

report = {
    "date": today,
    "open_price": round(open_price, 2),
    "close_price": round(close_price, 2),
    "change_pct": round(change_pct, 2),
    "volatility": round(volatility, 2)
}

# Sauvegarde dans le dossier Reports/DailyReports/
base_dir = os.path.dirname(os.path.abspath(__file__))
report_dir = os.path.join(base_dir, "DailyReports")
os.makedirs(report_dir, exist_ok=True)
output_path = os.path.join(report_dir, f"report-{today}.json")

with open(output_path, "w") as f:
    json.dump(report, f, indent=4)

print(f"[OK] Rapport généré : {output_path}")
