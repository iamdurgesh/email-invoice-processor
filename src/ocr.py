# src/ocr.py

from pdf2image import convert_from_path
import pytesseract

def extract_text_from_pdf(pdf_path):
    """
    Konvertiert eine PDF-Datei in Bilder und extrahiert Text aus jedem Bild mit pytesseract.
    
    Args:
        pdf_path (str): Pfad zur PDF-Datei.
    
    Rückgabe:
        str: Kombinierter Text, der aus allen Seiten der PDF-Datei extrahiert wurde.
        
    Anmerkung:
        - Stellen Sie sicher, dass „poppler“ auf Ihrem System installiert ist, damit pdf2image funktioniert.
    """
    try:
        # PDF-Seiten in eine Liste von Bildobjekten konvertieren.
        images = convert_from_path(pdf_path)
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return ""
    
    extracted_text = ""
    for image in images:
        # Extrahieren Sie Text aus jedem Bild mit Tesseract.
        page_text = pytesseract.image_to_string(image)
        extracted_text += page_text + "\n"
    
    return extracted_text
