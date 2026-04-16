import pytesseract
import cv2
import os

tesseract_path = os.getenv("TESSERACT_PATH")
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

def extract_text(image_path: str) -> str:
    """
    Extract text from image using OCR
    """
    image = cv2.imread(image_path)
    # Use a permissive OCR config so invoice punctuation and separators survive extraction.
    custom_config = r'--oem 3 --psm 4 -c preserve_interword_spaces=1'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text