from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import subprocess
import pandas as pd
import requests
import re
from subprocess import run
import time

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Allow all routes and credentials

# Configure SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'database.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Transaction Model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([{
        'id': t.id,
        'description': t.description,
        'amount': t.amount,
        'category': t.category,
        'date': t.date
    } for t in transactions])

from subprocess import Popen

def run_script(script_name):
    print(f"▶️ Launching {script_name}...")
    # Run the script without waiting for it to finish (fire and forget)
    Popen(["python", script_name])

def update_graphs():
    def update_script_save_path(script_path, output_filename):
        with open(script_path, 'r', encoding='utf-8') as file:
            content = file.read()

        updated_content = re.sub(
            r'pyo\.plot\(fig,\s*filename\s*=\s*"[^"]+"',
            f'pyo.plot(fig, filename="{output_filename}"',
            content
        )

        with open(script_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        print(f"✅ Updated {script_path} to save as {output_filename}")

    scripts = {
        "barplot.py": "barplot.html",
        "heatmap.py": "heatmap.html",
        "linechart.py": "linechart.html",
        "piechart.py": "piechart.html"
    }

    # First update the save paths in the scripts
    for script, output in scripts.items():
        update_script_save_path(script, output)

    # Start each script in parallel using Popen (fire and forget)
    for script in scripts:
        run_script(script)

    print("✅ All scripts have been launched in the background.")

from flask import send_from_directory

@app.route('/plot/<plot_type>')
def serve_plot(plot_type):
    filename_map = {
    "bar": "barplot.html",
    "line": "linechart.html",
    "pie": "piechart.html",
    "heatmap": "heatmap.html"
    }

    filename = filename_map.get(plot_type)
    if filename:
        return send_from_directory('.', filename)  # Current directory
    return "Plot not found", 404


@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    print("📥 Received transaction:", data)  # Log received data
    try:
        new_transaction = Transaction(
            description=data['description'],
            amount=data['amount'],
            category=data['category'],
            date=data['date']
        )
        db.session.add(new_transaction)
        db.session.commit()
        print(f"✅ Added transaction: {new_transaction.description}, ₹{new_transaction.amount}")

        update_graphs()  # Still regenerate graphs

        return jsonify({'message': 'Transaction added!', 'id': new_transaction.id}), 201
    except Exception as e:
        print("❌ Error while adding transaction:", e)
        return jsonify({'error': str(e)}), 500


@app.route('/transactions/<int:id>', methods=['DELETE', 'OPTIONS'])
def delete_transaction(id):
    if request.method == 'OPTIONS':  # Handle preflight request
        response = jsonify({'message': 'Preflight request successful'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'DELETE, GET, POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200
    
    transaction = Transaction.query.get(id)
    if transaction:
        db.session.delete(transaction)
        db.session.commit()
        print("🧠 Calling AI insight generator...\n")
        generate_insights()
        print("✅ AI insights function finished.\n")

        response = jsonify({'message': 'Transaction deleted successfully'})
    else:
        response = jsonify({'error': 'Transaction not found'}), 404

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/latest_plot/<plot_type>")
def latest_plot(plot_type):
    plot_dir = os.path.join(BASE_DIR, "static", "plots")

    # Ensure the directory exists
    if not os.path.exists(plot_dir):
        return jsonify({"error": "Plot directory does not exist"}), 404

    # Find the latest file matching the plot type
    files = sorted(
        [f for f in os.listdir(plot_dir) if plot_type in f],
        key=lambda x: os.path.getmtime(os.path.join(plot_dir, x)),
        reverse=True
    )

    if files:
        return send_from_directory(plot_dir, files[0])

    return jsonify({"error": "No plot found"}), 404

@app.route("/insights", methods=["GET"])
@app.route("/insights", methods=["POST"])
def fetch_insight():
    from flask import request

    try:
        data = request.get_json()
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        print(f"🔍 Received date range: {start_date} to {end_date}")

        insight = generate_insights(start_date, end_date)
        return jsonify({"insight": insight})
    except Exception as e:
        print("❌ Error in fetch_insight:", e)
        return jsonify({"insight": "Error processing the request."})

def generate_insights(start_date=None, end_date=None):
    from datetime import datetime
    import requests
    import json

    print("📊 Running generate_insights()")
    print("Filtering from:", start_date, "to:", end_date)

    transactions = Transaction.query.all()

    # Filter based on date range
    if start_date and end_date:
        transactions = [
            t for t in transactions
            if start_date <= t.date <= end_date
        ]

    data_by_week = {}
    for t in transactions:
        date_obj = datetime.strptime(t.date, "%Y-%m-%d")
        year_week = date_obj.strftime("%Y-W%U")
        if year_week not in data_by_week:
            data_by_week[year_week] = {}
        if t.category not in data_by_week[year_week]:
            data_by_week[year_week][t.category] = 0
        data_by_week[year_week][t.category] += t.amount

    # AI prompt generation
    trend_text = ""
    for week, cats in data_by_week.items():
        trend_text += f"{week}:\n"
        for cat, amt in cats.items():
            trend_text += f"  - {cat}: ₹{amt:.2f}\n"
        trend_text += "\n"

    prompt = f"Here is the user's weekly spending breakdown:\n{trend_text}\nGive a short trend analysis with recommendations."

    headers = {
        "Authorization": "Bearer sk- -- --- ",  # Use env var in prod # Open router API key
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a financial assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        output = res.json()
        insight = output["choices"][0]["message"]["content"]
        print("🧠 AI Insight:\n", insight)
        return insight
    except Exception as e:
        print("❌ Error fetching AI insights:", e)
        return "Error generating insight."


if __name__ == '__main__':
    app.run(debug=True, port=5000)
