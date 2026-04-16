from invoice_pipeline.extraction.data_extractor import extract_invoice_fields
from invoice_pipeline.ocr.ocr_engine import extract_text

if __name__ == "__main__":
    text = extract_text("data/processed/cleaned_page_0.jpg")

    result = extract_invoice_fields(text)
    print("Extracted Invoice Fields:")
    print(result)
