import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import datetime
import os
import json

app = Dash(__name__)
app.title = "BTC Live Dashboard"

# Charger les données du CSV
def load_data():
    df = pd.read_csv("../Scraper/btc_prices.csv", names=["datetime", "price"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df

# Charger le rapport journalier depuis Reports/DailyReports
def load_daily_report():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(base_dir, "..", "Reports", "DailyReports", f"report-{today}.json")
    print(f">>> Chemin rapport : {report_path}")
    print(f">>> Existe ? {os.path.exists(report_path)}")

    if os.path.exists(report_path):
        with open(report_path) as f:
            return json.load(f)
    return None

# Layout du dashboard
app.layout = html.Div([
    html.H1("Prix du Bitcoin (BTC/USDT)", style={"textAlign": "center"}),
    html.Div(id="last-price", style={"textAlign": "center", "fontSize": 28, "marginBottom": 20}),
    dcc.Graph(id="price-graph"),
    html.H2("Rapport journalier", style={"marginTop": 40, "textAlign": "center"}),
    html.Div(id="daily-report", style={"margin": "0 auto", "width": "60%", "fontSize": 18}),
    dcc.Interval(id="interval", interval=5*60*1000, n_intervals=0)
])

# Mise à jour automatique
@app.callback(
    [Output("last-price", "children"),
     Output("price-graph", "figure"),
     Output("daily-report", "children")],
    [Input("interval", "n_intervals")]
)
def update_dashboard(n):
    df = load_data()
    last_price = df.iloc[-1]["price"]

    fig = {
        "data": [{
            "x": df["datetime"],
            "y": df["price"],
            "type": "line",
            "name": "BTC Price"
        }],
        "layout": {
            "title": "Historique des prix",
            "xaxis": {"title": "Date"},
            "yaxis": {"title": "Prix (USDT)"}
        }
    }

    report = load_daily_report()
    if report:
        report_text = f"""
Date : {report['date']}  
Prix d'ouverture : {report['open_price']} USDT  
Prix de clôture : {report['close_price']} USDT  
Variation : {report['change_pct']}%  
Volatilité : {report['volatility']}
"""
    else:
        report_text = "Aucun rapport disponible pour aujourd'hui."

    return f"Dernier prix : {last_price} USDT", fig, report_text

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
