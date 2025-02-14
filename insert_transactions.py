import psycopg2
from psycopg2 import sql

# Define your database connection details
DB_HOST = "localhost"
DB_PORT = "5432"  # Default PostgreSQL port
DB_NAME = "momo_data"
DB_USER = "denaton"
DB_PASSWORD = " "

# Connect to the PostgreSQL database
def connect_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Insert cleaned and categorized data into the database
def insert_transaction(conn, transaction):
    try:
        with conn.cursor() as cursor:
            insert_query = """
            INSERT INTO transactions (category, transaction_date, transaction_time, amount, sms_transaction_id, sms_body)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (sms_transaction_id) DO NOTHING;
            """
            cursor.execute(insert_query, (
                transaction['category'],
                transaction['date'],
                transaction['time'],
                transaction['amount'],
                transaction['transaction_id'],
                transaction['body']
            ))
            conn.commit()
            print(f"Inserted transaction: {transaction['transaction_id']}")
    except Exception as e:
        print(f"Error inserting transaction: {e}")

# Example transactions (This will be your `transactions` list from the previous script)
transactions = [
    {
        "category": "Incoming Money",
        "date": "2025-02-12",
        "time": "14:30:00",
        "amount": 1000.00,
        "transaction_id": "12345",
        "body": "Received 1000 RWF from John. TxId: 12345"
    },
    {
        "category": "Payment to Code Holder",
        "date": "2025-02-13",
        "time": "15:45:00",
        "amount": 500.00,
        "transaction_id": "12346",
        "body": "Payment of 500 RWF to code holder. TxId: 12346"
    }
]

# Main function to insert all transactions
def main():
    conn = connect_db()
    if conn:
        for transaction in transactions:
            insert_transaction(conn, transaction)
        conn.close()

if __name__ == "__main__":
    main()
