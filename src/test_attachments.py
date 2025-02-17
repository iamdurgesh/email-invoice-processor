# src/test_attachments.py

from .email_processor import connect_to_mailbox, search_invoices, fetch_email
from .attachments import save_attachments

def test_all_attachments():
    # Connect to the mailbox
    mail = connect_to_mailbox()
    print("Connected to mailbox for attachment testing.")

    # Search for emails with 'Invoice' in the subject
    email_ids = search_invoices(mail)
    if not email_ids:
        print("No emails found with 'Invoice' in the subject.")
        return

    # Iterate through all found email IDs
    for email_id in email_ids:
        msg = fetch_email(mail, email_id)
        subject = msg.get("Subject")
        print(f"\nEmail ID: {email_id.decode()} | Subject: {subject}")
        
        # Save and list attachments from this email
        attachments = save_attachments(msg)
        if attachments:
            print("Attachments found:")
            for file in attachments:
                print(f"  {file}")
        else:
            print("No attachments found for this email.")

if __name__ == "__main__":
    test_all_attachments()
