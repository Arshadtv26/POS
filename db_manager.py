# db_manager.py
import mysql.connector

# Database connection
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Inoa2602@",
    "database": "POS"
}

def init_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS invoices (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        item_name VARCHAR(255),
                        quantity INT,
                        price DECIMAL(10, 2),
                        total DECIMAL(10, 2),
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')
    conn.commit()
    conn.close()

def save_invoice(item_name, quantity, price):
    total = quantity * price
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO invoices (item_name, quantity, price, total) VALUES (%s, %s, %s, %s)",
                   (item_name, quantity, price, total))
    conn.commit()
    conn.close()


def get_item_data():
    # Connect to the MySQL database
    conn = mysql.connector.connect(**db_config)

    # List to store the results
    items_data = []

    try:
        # Create a cursor to execute the SQL query
        cursor = conn.cursor()

        # SQL query to get item_name and item_price from items table
        query = "SELECT item_name, item_price FROM items"

        # Execute the query
        cursor.execute(query)

        # Fetch all results and store in list of tuples
        items_data = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

    return items_data

