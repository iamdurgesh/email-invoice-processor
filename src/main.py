import json
from .email_processor import connect_to_mailbox, search_invoices, fetch_email
from .attachments import save_attachments
from .ocr import extract_text_from_pdf
from .ai_extraction import extract_invoice_data
from .utils import get_email_text
from .db import get_db_client

def compile_email_text(msg, attachments):
    """
        Kombiniert Text aus dem E-Mail-Text mit Text, der aus PDF-Anhängen extrahiert wurde.
    """
    text = get_email_text(msg)
    for file_path in attachments:
        if file_path.lower().endswith('.pdf'):
            text += "\n" + extract_text_from_pdf(file_path)
    return text

def process_invoices():
    """
    Hauptverarbeitungsfunktion:
      - Verbindet sich mit der Mailbox,
      - Sucht nach Rechnungs-E-Mails,
      - Verarbeitet jede E-Mail (Abrufen, Speichern von Anhängen, Textextraktion, Extraktion von Rechnungsdaten),
      - Gibt alle Ergebnisse im JSON-Format aus.    
    """
    mail = connect_to_mailbox()
    email_ids = search_invoices(mail)
    all_invoices = []

    client = get_db_client()
    db = client.invoice_db

    for e_id in email_ids:
        msg = fetch_email(mail, e_id)
        attachments = save_attachments(msg)
        text = compile_email_text(msg, attachments)
        invoice_data = extract_invoice_data(text, msg)
        
        if invoice_data.get('invoice_number'):
            duplicate = db.invoices.find_one({
                "invoice_number": invoice_data.get("invoice_number"),
                "sender": invoice_data.get("sender")
            })
            if duplicate:
                print(f"Doppelte Rechnung gefunden: {invoice_data.get('invoice_number')}, Einfügen überspringen.")
            else:
                db.invoices.insert_one(invoice_data)
        
    # Abrufen der aktualisierten Liste der Rechnungen
    all_invoices = list(db.invoices.find({}, {"_id": 0}))


    with open("tests/test_output.json", "w") as f:
        json.dump(all_invoices, f, indent=4)

    print(json.dumps(all_invoices, indent=4))

if __name__ == '__main__':
    process_invoices()
