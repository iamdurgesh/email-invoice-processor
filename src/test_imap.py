# test_imap.py
from src.email_processor import connect_to_mailbox, search_invoices, fetch_email

def test_imap_connection():
    try:
        mail = connect_to_mailbox()
        print("Successfully connected to the mailbox!")
        
        email_ids = search_invoices(mail)
        print("Found email IDs:", email_ids)
        
        if email_ids:
            # Fetch the first email and print its subject for verification
            msg = fetch_email(mail, email_ids[0])
            print("Subject of the first email:", msg.get("Subject"))
        else:
            print("No emails found with 'Invoice' in the subject.")

    except Exception as e:
        print("An error occurred:", e)

if __name__ == '__main__':
    test_imap_connection()
