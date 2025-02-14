import xml.etree.ElementTree as ET
import re
import logging
from datetime import datetime

# Configure logging for unprocessed messages
logging.basicConfig(filename='unprocessed_sms.log', level=logging.WARNING, format='%(asctime)s - %(message)s')

# Parse XML file
tree = ET.parse('modified_sms_v2.xml')
root = tree.getroot()


# Function to extract amount from SMS body
def extract_amount(sms_body):
    match = re.search(r'([0-9]+[,.]?[0-9]*) RWF', sms_body)
    return int(match.group(1).replace(',', '')) if match else None


# Extract transaction ID from SMS body
def extract_transaction_id(sms_body):
    match = re.search(r'TxId[:\s]+(\d+)', sms_body)
    return match.group(1) if match else None


# Convert timestamp to readable date and time
def format_date(timestamp):
    try:
        dt = datetime.fromtimestamp(int(timestamp) / 1000)
        return dt.strftime('%Y-%m-%d'), dt.strftime('%H:%M:%S')
    except ValueError:
        return None, None


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

# Initialize data structure for relational database
transactions = []

# Process SMS data
for sms in root.findall('sms'):
    smsBody = sms.get('body', "")
    smsDate = sms.get('date')
    formattedDate, formattedTime = format_date(smsDate)
    amount = extract_amount(smsBody)
    transaction_id = extract_transaction_id(smsBody)

    # Ignore SMS without essential data
    if not smsBody or not formattedDate or amount is None:
        logging.warning(f"Unprocessed SMS: {smsBody}")
        continue

    category = "Text to ignore"
    for cat, keywords in categories.items():
        if any(keyword in smsBody for keyword in keywords):
            category = cat
            break

    transactions.append({
        "category": category,
        "date": formattedDate,
        "time": formattedTime,
        "amount": amount,
        "transaction_id": transaction_id,
        "body": smsBody
    })

# Print results (for preview)
for transaction in transactions:  # Display transactions for preview
    print(transaction)