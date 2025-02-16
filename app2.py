from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'momo_database',
    'auth_plugin': 'mysql_native_password'
}

# Function to connect to MySQL
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Example API endpoint
@app.route('/transactions', methods=['GET'])
def get_transactions():
    try:
        conn = get_db_connection()  # Use the get_db_connection function
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM momo_transaction ORDER BY sms_date DESC")  # Replace with your query
        transactions = cursor.fetchall()
        return jsonify(transactions)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Example insert endpoint (uncomment if needed)
# @app.route('/insert', methods=['POST'])
# def insert_data():
#     try:
#         data = request.json  # Get data from the frontend
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         query = "INSERT INTO your_table_name (column1, column2) VALUES (%s, %s)"
#         cursor.execute(query, (data['column1'], data['column2']))
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return jsonify({"message": "Data inserted successfully!"}), 201
#     except mysql.connector.Error as err:
#         return jsonify({"error": str(err)}), 500

if __name__ == '__main__':
    app.run(debug=True)
