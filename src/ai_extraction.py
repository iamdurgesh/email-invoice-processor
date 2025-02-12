from transformers import pipeline
import re

# Initialisieren Sie die rechnungsspezifische NER-Pipeline.
ner_model = pipeline("ner", model="drajend9/bert-finetuned-ner-invoice")

def ai_extract_invoice_data(text, sender):
    """
    Uses the invoice-specific NER model to extract key invoice details.
    
    Args:
        text (str): The combined text from the email and OCR.
        sender (str): The sender's email address.
        
    Returns:
        dict: Contains extracted fields: sender, invoice_number, total_amount, and due_date.
    """
    results = ner_model(text)

    
    data = {
        'sender': sender,
        'invoice_number': None,
        'total_amount': None,
        'due_date': None
    }
    
    # Process each recognized entity.
    for entity in results:
        label = entity['entity']
        word = entity['word']
        # label checks accordig to model's actual outputs.
        if label in ['B-INVOICE', 'I-INVOICE']:
            data['invoice_number'] = word
        elif label in ['B-TOTAL', 'I-TOTAL']:
            data['total_amount'] = word
        elif label in ['B-DATE', 'I-DATE']:
            data['due_date'] = word

    return data

def extract_invoice_data(text, msg):
    """
    Extracts invoice data using only the AI model.
    
    Args:
        text (str): Combined text from email and OCR.
        msg (email.message.Message): The email message object.
    
    Returns:
        dict: Extracted invoice details.
    """
    sender = msg.get('From')
    # Aufruf der AI-Extraktion
    data = ai_extract_invoice_data(text, sender)
    

    if not data['invoice_number']:
        match = re.search(r'INVOICE\s*(?:#|Number[:\s]*)\s*([A-Za-z0-9-]+)', text, re.IGNORECASE)
        if match:
            data['invoice_number'] = match.group(1)

    if not data['total_amount']:
        match = re.search(r'Total Amount[:\s]*\$?([\d,\.]+)', text, re.IGNORECASE)
        if match:
            data['total_amount'] = match.group(1)

    if not data['due_date']:
        match = re.search(r'Due Date[:\s]*([\d/\-]+)', text, re.IGNORECASE)
        if match:
            data['due_date'] = match.group(1)
    
    return data
