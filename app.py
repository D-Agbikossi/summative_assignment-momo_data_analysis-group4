from flask import Flask, jsonify, render_template, redirect, url_for
import mysql.connector
import logging
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import base64
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Simeon1405x",  
    "database": "momo_database",
    "auth_plugin": 'mysql_native_password'
}

def get_db_connection():
    """Create and return a MySQL database connection."""
    return mysql.connector.connect(**db_config)

def get_recent_transactions():
    """Fetch recent transactions from MySQL."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT transaction_id, category, sms_body, sms_date, sms_time, amount 
            FROM transactions 
            ORDER BY sms_date DESC 
            LIMIT 30
        """)
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        
        for transaction in transactions:
            if isinstance(transaction['sms_date'], datetime):
                transaction['sms_date'] = transaction['sms_date'].strftime('%Y-%m-%d %H:%M:%S')  
            if isinstance(transaction['sms_time'], timedelta):
                transaction['sms_time'] = transaction['sms_time'].total_seconds()  

        return transactions
    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}

@app.route('/get_transaction_summary')
def get_transaction_summary():
    """Fetch transaction summary from MySQL."""
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        outgoing_categories = (
            'Payment to Code Holder', 'Transfers to Mobile Numbers',
            'Airtime Bill Payments', 'Cash Power Bill Payments',
            'Transactions Initiated by Third Parties', 'Bank Transfers',
            'Internet and Voice Bundle Purchases'
        )
        
        queries = {
            "incomings": "SELECT COUNT(*) FROM transactions WHERE category = 'Incoming Money'",
            "outgoings": f"SELECT COUNT(*) FROM transactions WHERE category IN {outgoing_categories}",
            "withdrawals": "SELECT COUNT(*) FROM transactions WHERE category = 'Withdrawals from Agents'",
            "bills": "SELECT COUNT(*) FROM transactions WHERE category = 'Bank Deposits'"
        }
        
        counts = {}
        for key, query in queries.items():
            cursor.execute(query)
            counts[key] = cursor.fetchone()[0]
        
        return jsonify(counts)
        
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)})
    
    finally:
        cursor.close()
        db.close()

@app.route('/')
def home():
    """Redirect to the index page."""
    return redirect(url_for('index'))

@app.route('/index')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/statistics')
def statistics():
    """Render the statistics page with charts."""
    # Fetch data from the database
    conn = get_db_connection()
    query = "SELECT sms_date, amount, category FROM transactions WHERE amount IS NOT NULL"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Process data
    df = df.sort_values(by='sms_date')
    summary_df = df.groupby("category")["amount"].sum().reset_index()

    # Define category colors
    category_colors = {
        'Incoming Money': 'blue',
        'Payments to Code Holders': 'green',
        'Transfers to Mobile Numbers': 'red',
        'Bank Deposits': 'orange',
        'Airtime Bill Payments': 'purple',
        'Cash Power Bill Payments': 'yellow',
        'Transactions Initiated by Third Parties': 'cyan',
        'Withdrawals from Agents': 'pink',
        'Bank Transfers': 'brown',
        'Internet and Voice Bundle Purchases': 'gray',
        'Uncategorized': 'black',
    }

    # Generate scatter plot
    fig, ax = plt.subplots(figsize=(12, 6))
    for category, color in category_colors.items():
        subset = df[df['category'] == category]
        ax.scatter(subset.sms_date, subset.amount, label=category, color=color, alpha=0.7)
    ax.set_xlabel("Date")
    ax.set_ylabel("Transaction Amount (RWF)")
    ax.set_title("Mobile Money Transactions Categorised over Time")
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

    # Save scatter plot to base64
    img_bytes = BytesIO()
    fig.savefig(img_bytes, format='png', bbox_inches="tight")
    img_bytes.seek(0)
    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
    img_bytes.close()

    # Generate bar chart
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.barplot(x="amount", y="category", data=summary_df, palette=[category_colors[cat] for cat in summary_df['category']], ax=ax2)
    ax2.set_xlabel("Total Transaction Amount (RWF)")
    ax2.set_ylabel("Transaction Category")
    ax2.set_title("Total Mobile Money Transaction by Category")

    # Save bar chart to base64
    img_bytes2 = BytesIO()
    fig2.savefig(img_bytes2, format='png', bbox_inches="tight")
    img_bytes2.seek(0)
    img_base64_bar = base64.b64encode(img_bytes2.read()).decode('utf-8')
    img_bytes2.close()

    return render_template('statistics.html', img_base64=img_base64, img_base64_bar=img_base64_bar)

if __name__ == '__main__':
    app.run(debug=True, port=3000)