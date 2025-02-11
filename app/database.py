import psycopg2
from .. import config

def connect_to_db():
    """
    Connect to the PostgreSQL database using credentials from config.
    """
    try:
        conn = psycopg2.connect(
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT
        )
        return conn
    except Exception as e:
        print("Error connecting to database:", e)
        return None

def create_table():
    """
    Create the invoices table if it doesn't already exist.
    """
    conn = connect_to_db()
    if conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id SERIAL PRIMARY KEY,
                invoice_number TEXT UNIQUE,
                sender TEXT,
                amount TEXT,
                due_date TEXT,
                raw_text TEXT
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()

def is_duplicate_invoice(invoice_number: str) -> bool:
    """
    Check if a given invoice number already exists in the database.
    """
    conn = connect_to_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM invoices WHERE invoice_number = %s", (invoice_number,))
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count > 0
    return False

def save_invoice_to_db(invoice_data: dict):
    """
    Insert a new invoice record into the database.
    """
    conn = connect_to_db()
    if conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO invoices (invoice_number, sender, amount, due_date, raw_text) VALUES (%s, %s, %s, %s, %s)",
            (
                invoice_data["invoice_number"],
                invoice_data["sender"],
                invoice_data["amount"],
                invoice_data["due_date"],
                invoice_data["raw_text"]
            )
        )
        conn.commit()
        cur.close()
        conn.close()