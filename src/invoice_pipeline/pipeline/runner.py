from pathlib import Path
from invoice_pipeline.extraction.doc_classifier import detect_document_type
import json

from invoice_pipeline.preprocessing.image_cleaner import preprocess_image
from invoice_pipeline.ocr.ocr_engine import extract_text
from invoice_pipeline.extraction.data_extractor import extract_invoice_fields
from invoice_pipeline.ingestion.pdf_loader import convert_pdf_to_images
from invoice_pipeline.extraction.receipt_extractor import extract_receipt_fields

OCR_METHODS = ["adaptive", "otsu", "simple", "median"]

def compare_ocr_methods(
    image_path: str,
    doc_processed_dir: Path, 
    page_index: int
) -> dict:
    """
    Run OCR using each preprocessing method and keep the results side by side.

    This is mainly for experimentation and comparison of OCR results. I don't
    want the normal pipeline to run 4 OCR passes for every document.

    """
    ocr_results = {}

    for method in OCR_METHODS:
        cleaned_image_path = (
            doc_processed_dir / f"cleaned_page_{page_index}_{method}.jpg"
        )
        preprocess_image(
            image_path, 
            str(cleaned_image_path), 
            method=method
        )
        text = extract_text(str(cleaned_image_path))
        ocr_results[method] = {
            "image_path": str(cleaned_image_path),
            "extracted_text": text
        }
    return ocr_results

def process_single_pdf(
    pdf_path: str, 
    processed_root: str, 
    output_root: str
) -> dict:
    """
    Process one PDF from start to finish: convert to images, 
    preprocess, OCR, extract fields, and save results.

    """

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
        "document_type": None,
        "extracted_data": None,
        "error": None
    }

    try:
        # Step 1: Convert PDF to individual page images
        image_paths = convert_pdf_to_images(
            str(pdf_file), 
            str(doc_processed_dir)
        )
        all_text = []

        for i, image_path in enumerate(image_paths):
            # For normal processing I'm sticking with adaptive thresholding
            # for now. The compare_ocr_methods() function above can be used
            # separately when I want to investigate another method

            cleaned_image_path = (
                doc_processed_dir / f"cleaned_page_{i}.jpg"
            )
            # Step 2: Preprocess the image for better OCR accuracy
            preprocess_image(
                image_path, 
                str(cleaned_image_path), 
                method="adaptive"
            )   
            # Step 3: Extract text from the cleaned page
            text = extract_text(str(cleaned_image_path))
            all_text.append(text)

        # Combine all the pages before classification and field extraction. This is important for multi-page documents.
        # This keeps the extraction code independent of the number of pages in the invoice.
        combined_text = "\n".join(all_text)

        # print("\n=== Combined OCR Text ===\n")
        # print(combined_text)
        # print("\n===========END============\n")

        # Step 4: Identify document type and extract relevant fields
        doc_type = detect_document_type(combined_text)
        result["document_type"] = doc_type

        if doc_type == "invoice":
            result["extracted_data"] = extract_invoice_fields(combined_text)
        elif doc_type == "receipt":
            result["extracted_data"] = extract_receipt_fields(combined_text)
        else:
            result["status"] = "unsupported_document_type"
            result["error"] = (
                f"Document type '{doc_type}' is not supported for extraction."
            )

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

def process_folder(
    input_folder: str, 
    processed_root: str, 
    output_root: str
)-> list:
    input_dir = Path(input_folder)
    pdf_files = list(input_dir.rglob("*.pdf"))
    results = []

    for pdf_file in pdf_files:
        result = process_single_pdf(
            str(pdf_file), 
            processed_root, 
            output_root
        )
        results.append(result)

    return results