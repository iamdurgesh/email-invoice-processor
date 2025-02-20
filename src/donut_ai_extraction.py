# src/donut_extraction.py

from transformers import AutoProcessor, VisionEncoderDecoderModel
from PIL import Image

def extract_text_donut(image_path):
    """
    Uses the Donut model (naver-clova-ix/donut-base) to extract text from an invoice image.
    
    Args:
        image_path (str): Path to the invoice image (e.g., a PNG/JPEG file).
    
    Returns:
        str: The extracted text from the document.
    
    Note:
        - Donut is designed for document understanding and can capture layout information.
        - Ensure that you have installed the necessary packages:
              pip install transformers pillow torch
    """
    # Load the processor and model.
    processor = AutoProcessor.from_pretrained("naver-clova-ix/donut-base")
    model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base")
    
    # Open the image.
    image = Image.open(image_path).convert("RGB")
    
    # Preprocess the image.
    pixel_values = processor(image, return_tensors="pt").pixel_values
    
    # Generate the predicted text.
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    return generated_text
