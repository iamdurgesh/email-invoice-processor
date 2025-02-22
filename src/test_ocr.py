# src/test_ocr.py

from .ocr import extract_text_from_pdf

def test_pdf_ocr(pdf_path):
    """
    Extracts text from the specified PDF file and prints the result.
    """
    print(f"Testing OCR extraction on: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    print("\nExtracted text:\n")
    print(text)

if __name__ == "__main__":
    # Replace the path below with the path to a sample PDF you want to test.
    sample_pdf_path = "./attachments/invoice1.pdf"
    test_pdf_ocr(sample_pdf_path)
