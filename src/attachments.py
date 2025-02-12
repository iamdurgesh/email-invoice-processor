import os

ATTACHMENT_FOLDER = 'attachments'

def save_attachments(msg, download_folder=ATTACHMENT_FOLDER):
    """
    Speichert alle in der E-Mail-Nachricht gefundenen Anhänge in dem angegebenen Ordner.
    Gibt eine Liste der Dateipfade für die gespeicherten Anhänge zurück.
    """
    attachments = []
    # Wenn die E-Mail nicht mehrteilig ist, enthält sie keine Anhänge.
    if msg.get_content_maintype() != 'multipart':
        return attachments


    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        # Teile ohne Content-Disposition-Header überspringen
        if part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        if filename:
            # Erstellen Sie den Download-Ordner
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)
            filepath = os.path.join(download_folder, filename)
            with open(filepath, 'wb') as f:
                f.write(part.get_payload(decode=True))
            attachments.append(filepath)
    return attachments
