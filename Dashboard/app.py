import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import datetime

app = Dash(__name__)
app.title = "BTC Live Dashboard"

# Lire les données
def load_data():
    df = pd.read_csv("../Scraper/btc_prices.csv", names=["datetime", "price"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df

app.layout = html.Div([
    html.H1("Prix du Bitcoin (BTC/USDT)", style={"textAlign": "center"}),
    html.Div(id="last-price", style={"textAlign": "center", "fontSize": 28, "marginBottom": 20}),
    dcc.Graph(id="price-graph"),
    dcc.Interval(id="interval", interval=5*60*1000, n_intervals=0)  # maj toutes les 5 minutes
])

@app.callback(
    [Output("last-price", "children"),
     Output("price-graph", "figure")],
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
    return f"Dernier prix : {last_price} USDT", fig

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
