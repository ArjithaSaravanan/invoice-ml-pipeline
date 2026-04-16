from invoice_pipeline.ocr.ocr_engine import extract_text
import os

if __name__ == "__main__":

    image_path = "data/processed/cleaned_page_0.jpg"

    if os.path.exists(image_path):
        text = extract_text(image_path)
        print(f"Extracted Text:\n{text}")
    else:
        print(f"Warning: Cleaned image not found at {image_path}. Run preprocessing first")