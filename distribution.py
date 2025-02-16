import xml.etree.ElementTree as ET
import re
import logging
import mysql.connector
from datetime import datetime

# MySQL Connection Setup
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="momo_database",
    auth_plugin='mysql_native_password'
)
print("Connected to MySQL database!")
except mysql.connector.Error as err:
print(f"Error connecting to MySQL: {err}")
exit()
cursor = conn.cursor()

# Create the distribution table if it doesn't exist
create_distribution_table = """
CREATE TABLE IF NOT EXISTS distribution (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(255) UNIQUE,
    transaction_count INT DEFAULT 0
);
"""
cursor.execute(create_distribution_table)

# Define transaction categories
categories = {
    "Incoming Money": ["received"],
    "Payment to Code Holder": ["payment"],
    "Transfers to Mobile Numbers": ["transferred"],
    "Bank Deposits": ["deposit"],
    "Airtime Bill Payments": ["Airtime"],
    "Cash Power Bill Payments": ["Power"],
    "Transactions Initiated by Third Parties": ["transaction"],
    "Withdrawals from Agents": ["via agent"],
    "Bank Transfers": ["bank transfer"],
    "Internet and Voice Bundle Purchases": ["Bundles"]
}

# Sample transactions (replace this with real data parsing logic)
transactions = [
    {"category": "received"},
    {"category": "payment"},
    {"category": "transferred"},
    {"category": "deposit"},
    {"category": "Airtime"},
    {"category": "received"},
    {"category": "bank transfer"},
]

# Insert Transactions into MySQL
insert_transaction_query = """
INSERT INTO momo_transactions (category)
VALUES (%s)
"""
for transaction in transactions:
    try:
        cursor.execute(insert_transaction_query, (transaction["category"],))
    except Exception as e:
        logging.error(f"Error inserting transaction: {transaction['category']}\n{e}")

# Update Distribution Table (Category Counts)
update_distribution_query = """
INSERT INTO distribution (category, transaction_count)
VALUES (%s, %s)
ON DUPLICATE KEY UPDATE transaction_count = transaction_count + VALUES(transaction_count);
"""

# Count transactions per category
category_counts = {}
for transaction in transactions:
    category = transaction["category"]
    category_counts[category] = category_counts.get(category, 0) + 1

# Insert counts into distribution table
for category, count in category_counts.items():
    cursor.execute(update_distribution_query, (category, count))

# Commit and Close Connection
conn.commit()
cursor.close()
conn.close()

print("Transactions and category distribution successfully inserted into MySQL!")
