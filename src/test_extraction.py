# src/test_ai_extraction.py

import json
from email import message_from_string
from .ai_extraction import extract_invoice_data

def test_ai_extraction():
    # Sample text extracted from OCR (your invoice sample)
    sample_text = """
    ACME Corp.
    123 High Street, Some City

    Phone: 555-1234

    INVOICE #1023

    Bill To:
    John Doe
    45 Elm Street
    Some Other City

    Widget A 2 $50.00

    Widget B 3 $25.00

    Total Amount: 175.00

    Due Date: 03/15/2025

    Please make checks payable to ACME Corp.

    If you have any questions, contact us at billing@acmecorp.com.
    """

    # Create a simulated email message using the sample text.
    raw_email = f"From: billing@acmecorp.com\nSubject: Invoice\n\n{sample_text}"
    msg = message_from_string(raw_email)
    
    # Extract invoice data using our AI and regex fallback extraction.
    invoice_data = extract_invoice_data(sample_text, msg)
    
    print("Extracted Invoice Data:")
    print(json.dumps(invoice_data, indent=4))

if __name__ == "__main__":
    test_ai_extraction()
