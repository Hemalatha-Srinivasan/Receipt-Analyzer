import sqlite3

DB_NAME = "receipts.db"

# Initializes the database and creates the receipts table if it does not exist.
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Create receipts table with necessary fields
    c.execute('''
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor TEXT NOT NULL,
            date TEXT,
            amount REAL
        )
    ''')

    conn.commit()
    conn.close()


# Inserts a new receipt record into the database.
def insert_receipt(vendor, date, amount):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Parameterized query to prevent SQL injection
    c.execute(
        'INSERT INTO receipts (vendor, date, amount) VALUES (?, ?, ?)',
        (vendor, date, amount)
    )

    conn.commit()
    conn.close()


# Fetches all receipt records from the database.
def fetch_all_receipts():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Retrieve all records from receipts table
    c.execute('SELECT * FROM receipts')
    results = c.fetchall()

    conn.close()
    return results


# Deletes a receipt record by its ID.
def delete_receipt(receipt_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Delete the receipt with the specified ID
    c.execute('DELETE FROM receipts WHERE id = ?', (receipt_id,))

    conn.commit()
    conn.close()
