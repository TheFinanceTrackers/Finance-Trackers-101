import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import sqlite3

# Import your existing functions for each plot
from bar_plot import create_bar_chart
from backend.piechart import create_pie_chart
from heatmap import create_heatmap
from linechart import create_chart

# --- Initialize Dash ---
app = dash.Dash(__name__)

# --- Database Connection & Data Fetching ---
def fetch_data():
    conn = sqlite3.connect("database.sqlite")
    df = pd.read_sql_query("SELECT amount, category, date FROM 'transaction'", conn)
    conn.close()
    return df

df = fetch_data()

# --- Layout for Dashboard ---
app.layout = html.Div([
    html.H1("Finance Dashboard", style={'textAlign': 'center'}),
    
    dcc.Graph(id="bar-chart", figure=create_bar_chart(df)),
    dcc.Graph(id="pie-chart", figure=create_pie_chart(df)),
    dcc.Graph(id="heatmap", figure=create_heatmap(df)),
    dcc.Graph(id="line-chart", figure=create_chart(df)),
])

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
