from pathlib import Path
from invoice_pipeline.extraction.doc_classifier import detect_document_type
import json

from invoice_pipeline.preprocessing.image_cleaner import preprocess_image
from invoice_pipeline.ocr.ocr_engine import extract_text
from invoice_pipeline.extraction.data_extractor import extract_invoice_fields
from invoice_pipeline.ingestion.pdf_loader import convert_pdf_to_images
from invoice_pipeline.extraction.receipt_extractor import extract_receipt_fields

def process_single_pdf(pdf_path: str, processed_root: str, output_root: str) -> dict:
    pdf_file = Path(pdf_path)
    doc_name = pdf_file.stem

    doc_processed_dir = Path(processed_root) / doc_name
    doc_processed_dir.mkdir(parents=True, exist_ok=True)

    output_dir = Path(output_root)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "file_name": pdf_file.name,
        "document_id": doc_name,
        "status": "success",
        "extracted_data": None,
        "error": None
    }

    try:
        # Step 1: Convert PDF to images
        image_paths = convert_pdf_to_images(str(pdf_file), str(doc_processed_dir))
        all_text = []

        for i, image_path in enumerate(image_paths):
           
            cleaned_image_path = doc_processed_dir / f"cleaned_page_{i}.jpg"
            # Step 2: Preprocess the image
            preprocess_image(image_path, str(cleaned_image_path))
            # Step 3: Extract text using OCR
            text = extract_text(str(cleaned_image_path))
            all_text.append(text)
        
        combined_text = "\n".join(all_text)
        # Step 4: Extract structured fields
        doc_type = detect_document_type(combined_text)
        if doc_type == "invoice":
            extracted_data = extract_invoice_fields(combined_text)
        elif doc_type == "receipt":
            extracted_data = extract_receipt_fields(combined_text)
        else:
            extracted_data = extract_invoice_fields(combined_text)
        result["extracted_data"] = extracted_data

        #Step5: Save extracted data to JSON
        output_file = output_dir / f"{doc_name}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    except Exception as e:
        result["status"] = "failed"
        result["error"] = str(e)
        output_file = output_dir / f"{doc_name}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    return result

def process_folder(input_folder: str, processed_root: str, output_root: str)-> list:
    input_dir = Path(input_folder)
    pdf_files = list(input_dir.rglob("*.pdf"))
    results = []

    for pdf_file in pdf_files:
        result = process_single_pdf(str(pdf_file), processed_root, output_root)
        results.append(result)

    return results