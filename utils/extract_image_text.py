from PIL import Image
import pytesseract

def extract_text_from_image(image: Image.Image) -> str:
    """
    Extracts visible text from a PIL image using Tesseract OCR.
    Returns the extracted string.
    """
    try:
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"OCR Error: {str(e)}"
