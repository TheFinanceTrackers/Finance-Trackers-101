import sqlite3
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from datetime import datetime, timedelta

# --- Database Connection ---
def connect_to_db(db_file):
    return sqlite3.connect(db_file)

# --- Fetch Data from Database ---
def fetch_data_from_db(conn):
    query = """
    SELECT amount, category, date FROM "transaction"
    """
    return pd.read_sql_query(query, conn)

# --- Data Preparation ---
def prepare_data_for_plot(df):
    df["date"] = pd.to_datetime(df["date"])
    df_pivot = df.pivot_table(index="date", columns="category", values="amount", aggfunc="sum").fillna(0)
    return df_pivot

# --- Plotly Visualization ---
def create_bar_chart(df_pivot):
    colors = {
        "Housing": "#4173CD",       # Blue
        "Food": "#28A745",          # Green
        "Transportation": "#F0C419", # Yellow
        "Entertainment": "#A95BC0", # Purple
        "Healthcare": "#DC3545",    # Red
        "Shopping": "#E94E77",      # Pink
        "Others": "#808080"         # Gray
    }
    
    data = []
    for category in df_pivot.columns:
        data.append(
            go.Bar(
                x=df_pivot.index, 
                y=df_pivot[category],
                name=category,
                marker=dict(
                    color=colors.get(category, "#A9A9A9"),
                    line=dict(width=3, color="black")  # Thick black border
                ),
                hovertemplate=(
                    f"<b>{category}</b><br>"
                    "Date: %{x}<br>"
                    "Amount: %{y}<extra></extra>"
                )
            )
        )
    
    layout = go.Layout(
        title="Spending Categories Over Time",
        barmode="stack",
        xaxis=dict(
            tickangle=45,
            showgrid=True,
            tickformat="%b %d",
            zeroline=False,
            linecolor='rgba(0,0,0,0)'  # Remove axis border
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=True,
            gridcolor="lightgray",  # Soft grid lines
            zerolinecolor="gray"
        ),
        plot_bgcolor="rgba(255, 255, 255, 1)",
        paper_bgcolor="rgba(255, 255, 255, 1)",
        font=dict(
            family="Comic Sans MS, sans-serif",  # Cartoonish font
            size=14,
            color="black"
        ),
        legend=dict(
            title="Categories",
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.2
        )
    )
    
    fig = go.Figure(data=data, layout=layout)
    return fig

# --- Main Execution ---
if __name__ == "__main__":
    db_connection = connect_to_db("database.sqlite")
    df = fetch_data_from_db(db_connection)
    db_connection.close()
    df_pivot = prepare_data_for_plot(df)
    fig = create_bar_chart(df_pivot)
    pyo.plot(fig, filename="barplot.html", auto_open=False)
