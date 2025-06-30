from transformers import pipeline
from PIL import Image

# Load once (global or in function)
ocr_pipeline = pipeline("image-to-text", model="microsoft/trocr-base-printed")

def extract_text_from_image(image: Image.Image) -> str:
    result = ocr_pipeline(image)
    return result[0]["generated_text"] if result else ""
