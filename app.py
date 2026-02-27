import pandas as pd

df = pd.read_csv("data.csv")
df["date"] = pd.to_datetime(df["date"])

import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.H1("Fitness Dashboard")

if __name__ == "__main__":
    app.run(debug=True)