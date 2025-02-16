from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import io
import base64
from io import BytesIO

app = Flask(__name__)

# MySQL Database connection setup
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="momo_database",
        auth_plugin='mysql_native_password'
    )
    return conn

@app.route('/')
def index():
    # Setup MySQL connection
    conn = get_db_connection()

    # Query to fetch data from the database
    query = "SELECT sms_data, amount, category FROM momo_transactions WHERE amount IS NOT NULL"
    df = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    # Convert "sms_data" to datetime format
    df['sms_data'] = pd.to_datetime(df['sms_data'])
    df = df.sort_values(by='sms_data')

    # Aggregate data by category
    summary_df = df.groupby("category")["amount"].sum().reset_index()

    # Define category colors for the scatter plot
    category_colors = {
        "Incoming money": "green",
        "Payment to Code Holder": "red",
        "Transfer to Mobile Numbers": "blue",
        "Bank Deposits": "orange",
        "Airtime Bill Payments": "purple",
        "Cash Power Bill Payments": "brown",
        "Transaction Initiated by Third Parties": "pink",
        "Withdrawals from Agents": "black",
        "Bank Transfers": "yellow",
        "Internet and Voice Bundle Purchases": "cyan"
    }

    # Generate scatter plot
    fig, ax = plt.subplots(figsize=[12, 6])
    for category, color in category_colors.items():
        subset = df[df['category'] == category]
        ax.scatter(subset.sms_data, subset.amount, label=category, color=color, alpha=0.7)
    ax.set_xlabel("Date")
    ax.set_ylabel("Transaction Amount (RWF)")
    ax.set_title("Mobile Money Transactions Categorised over Time")
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

    # Save scatter plot to BytesIO object
    img_bytes = BytesIO()
    fig.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    # Encode scatter plot to base64
    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

    # Plotting bar chart
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.barplot(x="amount", y="category", data=summary_df, palette=category_colors, ax=ax2)
    ax2.set_xlabel("Total Transaction Amount (RWF)")
    ax2.set_ylabel("Transaction Category")
    ax2.set_title("Total Mobile Money Transaction by Category")

    # Save bar plot to BytesIO object
    img_bytes2 = BytesIO()
    fig2.savefig(img_bytes2, format='png')
    img_bytes2.seek(0)

    # Encode bar plot to base64
    img_base64_bar = base64.b64encode(img_bytes2.read()).decode('utf-8')

    # Return the rendered HTML template with the embedded plots
    return render_template('index.html', img_base64=img_base64, img_base64_bar=img_base64_bar)


if __name__ == '__main__':
    app.run(debug=True)
