# src/test_donut.py

from .donut_ai_extraction import extract_text_donut

def test_donut_extraction():
    image_path = "attachments/invoice1.pdf"  # Replace with your image file path.
    extracted_text = extract_text_donut(image_path)
    print("Extracted text using Donut:")
    print(extracted_text)

if __name__ == "__main__":
    test_donut_extraction()
