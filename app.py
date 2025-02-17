from flask import Flask, jsonify
from flask import Flask, render_template
import mysql.connector
import logging
from datetime import timedelta, datetime  
from distribution import update_distribution

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Simeon1405x",  
    "database": "momo_database"
}

def get_recent_transactions():
    """Fetch recent transactions from MySQL"""
    try:
        conn = mysql.connector.connect(**db_config)
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

import mysql.connector

db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Simeon1405x",
    "database": "momo_database"
}

@app.route('/get_transaction_summary')
def get_transaction_summary():
    try:
        db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Simeon1405x",
            database="momo_database"
        )
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
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)