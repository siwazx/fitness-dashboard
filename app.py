import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# -------------------------
# Load Dataset
# -------------------------
df = pd.read_csv("data.csv")

# ทำให้ชื่อคอลัมน์เป็นตัวเล็กทั้งหมด ป้องกันพังจากตัวใหญ่เล็ก
df.columns = df.columns.str.lower()

# แปลงวันที่
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

df = df.sort_values("date")

print("Columns:", df.columns)
print("Total rows:", len(df))

app = dash.Dash(__name__)

# -------------------------
# Layout
# -------------------------
app.layout = html.Div([

    html.H1(
        "🏋️ Fitness Tracking Dashboard",
        style={"textAlign": "center", "marginBottom": "20px"}
    ),

    dcc.Dropdown(
        id="date-range",
        options=[
            {"label": "Last 7 Days", "value": "7"},
            {"label": "Last 30 Days", "value": "30"},
            {"label": "All", "value": "all"},
        ],
        value="all",
        clearable=False,
        style={"width": "50%", "margin": "auto"}
    ),

    html.Br(),

    html.Div(
        id="summary",
        style={
            "display": "flex",
            "justifyContent": "center",
            "gap": "20px",
            "marginBottom": "30px"
        }
    ),

    dcc.Graph(id="graph1"),
    dcc.Graph(id="graph2"),
    dcc.Graph(id="graph3"),
    dcc.Graph(id="weight-trend-chart"),

    html.P(
        "This dashboard helps track weight and calorie trends over time.",
        style={"textAlign": "center", "marginTop": "20px"}
    )

], style={
    "backgroundColor": "#f5f5f5",
    "padding": "30px"
})

# -------------------------
# Callback
# -------------------------
@app.callback(
    Output("graph1", "figure"),
    Output("graph2", "figure"),
    Output("graph3", "figure"),
    Output("weight-trend-chart", "figure"),
    Output("summary", "children"),
    Input("date-range", "value")
)
def update_dashboard(selected_range):

    # Filter Data
    if selected_range == "7":
        filtered_df = df.tail(7)
    elif selected_range == "30":
        filtered_df = df.tail(30)
    else:
        filtered_df = df

    # ถ้าไม่มีข้อมูล
    if filtered_df is None or filtered_df.empty:
        empty_fig = px.line(title="No data available")
        return empty_fig, empty_fig, empty_fig, empty_fig, []

    try:
        # Graph 1 - Weight Over Time
        fig1 = px.line(
            filtered_df,
            x="date",
            y="weight",
            title="Weight Over Time",
            markers=True
        )

        # Graph 2 - Daily Calories
        fig2 = px.bar(
            filtered_df,
            x="date",
            y="calories",
            title="Daily Calories"
        )

        # Graph 3 - Calories vs Weight
        fig3 = px.scatter(
            filtered_df,
            x="calories",
            y="weight",
            hover_data=["date"],
            title="Calories vs Weight"
        )

        # Graph 4 - Detailed Weight Trend
        weight_fig = px.line(
            filtered_df,
            x="date",
            y="weight",
            title="Weight Trend Detail",
            markers=True
        )

        # Summary Calculations
        latest_weight = filtered_df["weight"].iloc[-1]
        avg_calories = round(filtered_df["calories"].mean(), 2)
        total_entries = len(filtered_df)
        weight_change = round(
            filtered_df["weight"].iloc[-1] - filtered_df["weight"].iloc[0], 2
        )

        summary_cards = [
            html.Div(f"Latest Weight: {latest_weight} kg"),
            html.Div(f"Average Calories: {avg_calories}"),
            html.Div(f"Entries: {total_entries}"),
            html.Div(f"Weight Change: {weight_change} kg"),
        ]

        return fig1, fig2, fig3, weight_fig, summary_cards

    except Exception as e:
        print("ERROR:", e)
        empty_fig = px.line(title="Error occurred")
        return empty_fig, empty_fig, empty_fig, empty_fig, []

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)