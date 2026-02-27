import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# โหลดข้อมูล
df = pd.read_csv("data.csv")
df["date"] = pd.to_datetime(df["date"])

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Fitness Dashboard"),

    dcc.Dropdown(
        id="date-range",
        options=[
            {"label": "Last 7 Days", "value": "7"},
            {"label": "Last 30 Days", "value": "30"},
            {"label": "All", "value": "all"},
        ],
        value="all",
        clearable=False
    ),

    dcc.Graph(id="graph1"),
    dcc.Graph(id="graph2"),
    dcc.Graph(id="graph3")
])


@app.callback(
    Output("graph1", "figure"),
    Output("graph2", "figure"),
    Output("graph3", "figure"),
    Input("date-range", "value")
)
def update_graphs(selected_range):

    if selected_range == "7":
        filtered_df = df.sort_values("date").tail(7)
    elif selected_range == "30":
        filtered_df = df.sort_values("date").tail(30)
    else:
        filtered_df = df

    fig1 = px.line(filtered_df, x="date", y="weight",
                   title="Weight Over Time")

    fig2 = px.bar(filtered_df, x="date", y="calories",
                  title="Daily Calories")

    fig3 = px.scatter(filtered_df, x="calories", y="weight",
                      title="Calories vs Weight")

    return fig1, fig2, fig3


if __name__ == "__main__":
    app.run(debug=True)