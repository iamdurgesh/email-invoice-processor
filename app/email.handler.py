import imaplib
import email
import os
from email.header import decode_header

from . import config
from .ocr_utils import extract_invoice_data
from .invoice_extractor import email_is_invoice_candidate

def connect_to_email():
    """
    Connect to the IMAP server using credentials from config.
    """
    try:
        mail = imaplib.IMAP4_SSL(config.IMAP_SERVER, config.IMAP_PORT)
        mail.login(config.EMAIL_ACCOUNT, config.EMAIL_PASSWORD)
        mail.select("inbox")  # or the folder you want to check
        return mail
    except Exception as e:
        print("Error connecting to email:", e)
        return None

def search_invoices(mail) -> list:
    """
    Search emails in the mailbox, filter them using a heuristic, 
    and return a list of IDs that are likely invoices.
    """
    invoice_email_ids = []
    try:
        result, data = mail.search(None, 'ALL')
        if result == "OK":
            email_ids = data[0].split()
            print(f"Found {len(email_ids)} total emails. Checking for invoices...")

            for eid in email_ids:
                res, msg_data = mail.fetch(eid, "(RFC822)")
                if res != "OK":
                    continue

                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        subject = subject.decode(encoding) if encoding else subject

                        # Use a heuristic or AI-based function to check if it's an invoice
                        if email_is_invoice_candidate(subject):
                            invoice_email_ids.append(eid)

        print(f"Identified {len(invoice_email_ids)} potential invoice emails.")
        return invoice_email_ids

    except Exception as e:
        print("Error searching emails:", e)
        return []

def process_emails(mail, email_ids):
    """
    For each email ID identified as an invoice candidate, download and process attachments.
    """
    invoice_folder = "invoices"
    os.makedirs(invoice_folder, exist_ok=True)

    for email_id in email_ids:
        result, msg_data = mail.fetch(email_id, "(RFC822)")
        if result != "OK":
            continue

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
