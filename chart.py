from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import mysql.connector
import base64
from io import BytesIO

app = Flask(__name__)

# MySQL Database connection setup
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Simeon1405x",
        database="momo_database",
        auth_plugin='mysql_native_password'
    )
    return conn

@app.route('/statistics')
def statistics():
    conn = get_db_connection()
    query = "SELECT sms_date, amount, category FROM transactions WHERE amount IS NOT NULL"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Check data types
    print(df.dtypes)

    # Inspect data
    print(df.head())
    print(df['amount'].head())

    df = df.sort_values(by='sms_date')
    summary_df = df.groupby("category")["amount"].sum().reset_index()

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

    for category in summary_df['category'].unique():
        if category not in category_colors:
            category_colors[category] = 'gray'

    fig, ax = plt.subplots(figsize=(12, 6))
    for category, color in category_colors.items():
        subset = df[df['category'] == category]
        ax.scatter(subset.sms_date, subset.amount, label=category, color=color, alpha=0.7)
    ax.set_xlabel("Date")
    ax.set_ylabel("Transaction Amount (RWF)")
    ax.set_title("Mobile Money Transactions Categorised over Time")
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
    ax.ticklabel_format(style='plain', axis='y')  # Ensure y-axis uses plain format

    img_bytes = BytesIO()
    fig.savefig(img_bytes, format='png', bbox_inches="tight")
    img_bytes.seek(0)
    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
    img_bytes.close()

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.barplot(x="amount", y="category", data=summary_df, palette=[category_colors[cat] for cat in summary_df['category']], ax=ax2)
    ax2.set_xlabel("Total Transaction Amount (RWF)")
    ax2.set_ylabel("Transaction Category")
    ax2.set_title("Total Mobile Money Transaction by Category")
    ax2.ticklabel_format(style='plain', axis='x')  # Ensure x-axis uses plain format

    img_bytes2 = BytesIO()
    fig2.savefig(img_bytes2, format='png', bbox_inches="tight")
    img_bytes2.seek(0)
    img_base64_bar = base64.b64encode(img_bytes2.read()).decode('utf-8')
    img_bytes2.close()

    return render_template('statistics.html', img_base64=img_base64, img_base64_bar=img_base64_bar)

@app.route('/')
def home():
    return redirect(url_for('index'))  # Redirect to /index

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)