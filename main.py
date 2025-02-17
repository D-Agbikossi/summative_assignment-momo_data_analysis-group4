import xml.etree.ElementTree as ET
import re
import logging
import mysql.connector
from datetime import datetime


logging.basicConfig(filename='unprocessed_sms.log', level=logging.WARNING, format='%(asctime)s - %(message)s')


tree = ET.parse('modified_sms_v2.xml')
root = tree.getroot()


def extract_amount(sms_body):
    match = re.search(r'([0-9]+[,.]?[0-9]*) RWF', sms_body)
    return int(match.group(1).replace(',', '')) if match else None


def extract_transaction_id(sms_body):
    match = re.search(r'TxId[:\s]+(\d+)|Financial Transaction Id[:\s]+(\d+)', sms_body)
    if match:
        return match.group(1) if match.group(1) else match.group(2)
    
    return None


def format_date(timestamp):
    if not timestamp:
        return None, None 
    try:
        dt = datetime.fromtimestamp(int(timestamp) / 1000)
        return dt.strftime('%Y-%m-%d'), dt.strftime('%H:%M:%S')
    except ValueError:
        return None, None


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


def determine_transaction_type(category):
    if category == "Incoming Money":
        return "incomings"
    elif category in [
        "Payment to Code Holder",
        "Transfers to Mobile Numbers",
        "Airtime Bill Payments",
        "Cash Power Bill Payments",
        "Transactions Initiated by Third Parties",
        "Bank Transfers",
        "Internet and Voice Bundle Purchases"
    ]:
        return "outgoings"
    elif category == "Withdrawals from Agents":
        return "withdrawals"
    elif category == "Bank Deposits":
        return "bills"
    else:
        return "uncategorized"
    

transactions = []


for sms in root.findall('sms'):
    sms_body = sms.get('body', "")
    sms_date = sms.get('date')
    formatted_date, formatted_time = format_date(sms_date)
    amount = extract_amount(sms_body)
    transaction_id = extract_transaction_id(sms_body) or "N/A"  

    
    if not sms_body or not formatted_date or amount is None:
        logging.warning(f"Unprocessed SMS: {sms_body}")
        continue


    category = "Uncategorized"
    for cat, keywords in categories.items():
        if any(re.search(rf'\b{kw}\b', sms_body, re.IGNORECASE) for kw in keywords):
            category = cat
            break

    
    transaction_type = determine_transaction_type(category)

    transactions.append({
        "category": category,
        "date": formatted_date,
        "time": formatted_time,
        "amount": amount,
        "transaction_id": transaction_id,
        "body": sms_body,
        "type": transaction_type
    })


try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Simeon1405x",
        database="momo_database",
        auth_plugin='mysql_native_password'
    )
    print("Connected to MySQL database!")
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    exit()
cursor = conn.cursor()


create_table_query = """
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(50) NULL,
    category VARCHAR(255),
    sms_body TEXT,
    sms_date DATE,
    sms_time TIME,
    amount DECIMAL(10,2),
    type VARCHAR(50)
);
"""
cursor.execute(create_table_query)
conn.commit()


insert_query = """
    INSERT INTO transactions (transaction_id, category, sms_body, sms_date, sms_time, amount, type)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

for transaction in transactions:
    try:
        cursor.execute(insert_query, (
            transaction["transaction_id"],
            transaction["category"],
            transaction["body"],
            transaction["date"],
            transaction["time"],
            transaction["amount"],
            transaction["type"]
        ))
    except Exception as e:
        logging.error(f"Error inserting transaction: {transaction['body']}\n{e}")


conn.commit()
cursor.close()
conn.close()

print("Transactions successfully inserted into MySQL!")
