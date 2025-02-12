# src/utils.py

def get_email_text(msg):
    """
 Extrahiert und dekodiert den Klartextinhalt aus einer E-Mail-Nachricht.
    Gibt den Inhalt des Textes zurück.
    """
    text = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    text += payload.decode('utf-8', errors='ignore')
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            text = payload.decode('utf-8', errors='ignore')
    return text
