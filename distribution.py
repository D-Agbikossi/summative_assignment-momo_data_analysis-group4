import mysql.connector
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_distribution():
    """
    Creates the distribution table (if it doesn't exist) with four columns:
      - incomings: count of transactions where category is 'Incoming Money'
      - outgoings: count of transactions for payment-related categories:
            'Payment to Code Holder', 'Transfers to Mobile Numbers',
            'Airtime Bill Payments', 'Cash Power Bill Payments',
            'Transactions Initiated by Third Parties', 'Bank Transfers',
            'Internet and Voice Bundle Purchases'
      - withdrawals: count of transactions where category is 'Withdrawals from Agents'
      - bills: count of transactions where category is 'Bank Deposits'
    Then, updates the single summary row (id = 1) with these counts.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Simeon1405x",
            database="momo_database",
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor()

        # Create the distribution table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS distribution (
            id INT PRIMARY KEY,
            incomings INT DEFAULT 0,
            outgoings INT DEFAULT 0,
            withdrawals INT DEFAULT 0,
            bills INT DEFAULT 0
        )
        """
        cursor.execute(create_table_query)
        conn.commit()

        # Ensure a single summary row exists with id = 1
        insert_row_query = """
        INSERT IGNORE INTO distribution (id, incomings, outgoings, withdrawals, bills)
        VALUES (1, 0, 0, 0, 0)
        """
        cursor.execute(insert_row_query)
        conn.commit()

        # Update distribution counts using subqueries from the transactions table
        update_query = """
        UPDATE distribution
        SET 
            incomings = (
                SELECT COUNT(*) FROM transactions
                WHERE transactions.category = 'Incoming Money'
            ),
            outgoings = (
                SELECT COUNT(*) FROM transactions
                WHERE transactions.category IN (
                    'Payment to Code Holder', 
                    'Transfers to Mobile Numbers',
                    'Airtime Bill Payments',
                    'Cash Power Bill Payments',
                    'Transactions Initiated by Third Parties',
                    'Bank Transfers',
                    'Internet and Voice Bundle Purchases'
                )
            ),
            withdrawals = (
                SELECT COUNT(*) FROM transactions
                WHERE transactions.category = 'Withdrawals from Agents'
            ),
            bills = (
                SELECT COUNT(*) FROM transactions
                WHERE transactions.category = 'Bank Deposits'
            )
        WHERE id = 1
        """
        cursor.execute(update_query)
        conn.commit()

        cursor.close()
        conn.close()
        logger.info("Distribution table updated successfully.")
    except mysql.connector.Error as err:
        logger.error(f"Database error in update_distribution: {err}")
        raise
    except Exception as e:
        logger.error(f"General error in update_distribution: {e}")
        raise

if __name__ == '__main__':
    update_distribution()
    print("Distribution updated successfully.")