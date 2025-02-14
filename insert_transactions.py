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


# Main function to insert all transactions
def main():
    conn = connect_db()
    if conn:
        for transaction in transactions:
            insert_transaction(conn, transaction)
        conn.close()

if __name__ == "__main__":
    main()
