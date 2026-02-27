import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# โหลดข้อมูล
df = pd.read_csv("data.csv")
df["date"] = pd.to_datetime(df["date"])

# สร้างกราฟทั้ง 3 ตัว
fig1 = px.line(df, x="date", y="weight", title="Weight Over Time")
fig2 = px.bar(df, x="date", y="calories", title="Daily Calories")
fig3 = px.scatter(df, x="steps", y="workout_minutes",
                  title="Steps vs Workout Minutes")

app = dash.Dash(__name__)

# 🔥 ตรงนี้แหละที่เรียกว่า layout
app.layout = html.Div([
    html.H1("Fitness Dashboard"),

    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3)
])

if __name__ == "__main__":
    app.run(debug=True)