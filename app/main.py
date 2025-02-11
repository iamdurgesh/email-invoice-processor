import imaplib
import email
import os
import pytesseract
import pdf2image
import re
import json
import psycopg2
from email.header import decode_header
from PyPDF2 import PdfReader
from fastapi import FastAPI

# Email account credentials (update these with your credentials)
EMAIL_ACCOUNT = "your-email@example.com"
EMAIL_PASSWORD = "your-email-password"
IMAP_SERVER = "imap.gmail.com"  # Change for other providers
IMAP_PORT = 993

# Database credentials (update these accordingly)
DB_NAME = "invoice_db"
DB_USER = "postgres"
DB_PASSWORD = "your-db-password"
DB_HOST = "localhost"
DB_PORT = "5432"

# Initialize FastAPI
app = FastAPI()

# Connect to the PostgreSQL database
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        return conn
    except Exception as e:
        print("Error connecting to database:", e)
        return None

# Create table if not exists
def create_table():
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

# Connect to email inbox
def connect_to_email():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")  # Select the inbox
        return mail
    except Exception as e:
        print("Error connecting to email:", e)
        return None

# Search for emails with potential invoices
def search_invoices(mail):
    try:
        result, data = mail.search(None, 'ALL')  # Fetch all emails (modify if needed)
        email_ids = data[0].split()
        print(f"Found {len(email_ids)} emails.")
        return email_ids
    except Exception as e:
        print("Error searching emails:", e)
        return []

# Process each email and download attachments
def process_emails(mail, email_ids):
    invoice_folder = "invoices"  # Folder to store invoices
    os.makedirs(invoice_folder, exist_ok=True)
    
    for email_id in email_ids:
        result, msg_data = mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                subject = subject.decode(encoding) if encoding else subject
                sender = msg.get("From")
                
                print(f"Processing email from {sender} - Subject: {subject}")
                
                # Check for attachments
                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get("Content-Disposition") is None:
                        continue
                    
                    filename = part.get_filename()
                    if filename:
                        filepath = os.path.join(invoice_folder, filename)
                        with open(filepath, "wb") as f:
                            f.write(part.get_payload(decode=True))
                        print(f"Saved attachment: {filename}")
                        
                        # Process PDF for invoice extraction
                        if filename.lower().endswith(".pdf"):
                            extract_invoice_data(filepath, sender)

# Extract invoice details from PDF
def extract_invoice_data(pdf_path, sender):
    try:
        images = pdf2image.convert_from_path(pdf_path)
        extracted_text = ""
        for image in images:
            extracted_text += pytesseract.image_to_string(image) + "\n"
        
        print("Extracted Text from Invoice:")
        print(extracted_text)
        
        # Extract key details
        invoice_data = extract_key_details(extracted_text)
        invoice_data["sender"] = sender
        invoice_data["raw_text"] = extracted_text
        
        # Check for duplicates before saving
        if not is_duplicate_invoice(invoice_data["invoice_number"]):
            save_invoice_to_db(invoice_data)
            print(json.dumps(invoice_data, indent=4))
        else:
            print("Duplicate invoice detected. Skipping storage.")
        
    except Exception as e:
        print(f"Error extracting data from {pdf_path}: {e}")

# Extract key details using regex
def extract_key_details(text):
    invoice_number = re.search(r"Invoice[\s#:]*([A-Za-z0-9-]+)", text, re.IGNORECASE)
    amount = re.search(r"Total[\sAmount:]*([\d,]+\.\d{2})", text, re.IGNORECASE)
    due_date = re.search(r"Due[\sDate:]*([\d/\-]+)", text, re.IGNORECASE)
    
    return {
        "invoice_number": invoice_number.group(1) if invoice_number else "Not found",
        "amount": amount.group(1) if amount else "Not found",
        "due_date": due_date.group(1) if due_date else "Not found"
    }

# Save extracted invoice data to PostgreSQL
def save_invoice_to_db(invoice_data):
    conn = connect_to_db()
    if conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO invoices (invoice_number, sender, amount, due_date, raw_text) VALUES (%s, %s, %s, %s, %s)",
            (invoice_data["invoice_number"], invoice_data["sender"], invoice_data["amount"], invoice_data["due_date"], invoice_data["raw_text"])
        )
        conn.commit()
        cur.close()
        conn.close()

# API Endpoint to fetch stored invoices
@app.get("/invoices")
def get_invoices():
    conn = connect_to_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT invoice_number, sender, amount, due_date, raw_text FROM invoices")
        invoices = cur.fetchall()
        cur.close()
        conn.close()
        return {"invoices": [
            {"invoice_number": row[0], "sender": row[1], "amount": row[2], "due_date": row[3], "raw_text": row[4]}
            for row in invoices
        ]}
    return {"error": "Unable to fetch invoices"}

if __name__ == "__main__":
    create_table()
    mail = connect_to_email()
    if mail:
        email_ids = search_invoices(mail)
        if email_ids:
            process_emails(mail, email_ids)
        mail.logout()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
