import imaplib
import email
import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

# IMAP-Server und Anmeldedaten aus Umgebungsvariablen abrufen
IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
PASSWORD = os.getenv("PASSWORD")
MAILBOX = os.getenv("MAILBOX", "INBOX")  # Standardwert ist INBOX

def connect_to_mailbox():
    """
    Verbindet sich mit dem IMAP-Server, meldet sich an und wählt das Postfach aus.
    Gibt das IMAP-Verbindungsobjekt zurück.
    """
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.select(MAILBOX)
    return mail

def search_invoices(mail):
    """
    Sucht nach E-Mails mit 'Invoice' im Betreff.
    Gibt eine Liste von E-Mail-IDs zurück.
    """
    status, data = mail.search(None, '(SUBJECT "Invoice")')
    email_ids = data[0].split()
    return email_ids

def fetch_email(mail, email_id):
    """
    Ruft eine E-Mail anhand ihrer ID ab und analysiert sie.
    Gibt ein email.message.Message-Objekt zurück.
    """
    status, data = mail.fetch(email_id, '(RFC822)')
    raw_email = data[0][1]
    return email.message_from_bytes(raw_email)

