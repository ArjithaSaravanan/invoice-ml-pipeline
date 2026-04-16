import re
from typing import List, Dict
from invoice_pipeline.extraction.cleaner import clean_text, clean_number

def extract_invoice_fields(text: str) -> Dict:
    """
    Extract structured invoice fields from the OCR text
    """
    result = {
        "invoice_number": None,
        "date": None,
        "total_amount": None,
        "items": []
    }

    invoice_number_match = re.search(r"Invoice\s*Number[:\s]*([A-Za-z0-9-]+)", text)
    if invoice_number_match:
        result["invoice_number"] = invoice_number_match.group(1)

    date_match = re.search(r"Date:\s*([\d-]+)", text)
    if date_match:
        result["date"] = date_match.group(1)

    total_match = re.search(r"Total\s*Amount:\s*€?(\d+)", text)
    if total_match:
        result["total_amount"] = total_match.group(1)

    lines = text.splitlines()
    for line in lines:
        if "|" in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]

            if len(parts) >= 4:
                item = clean_text(parts[0])
                qty = clean_number(parts[1])
                price = clean_number(parts[2])
                total = clean_number(parts[3])

                if qty and price:
                    result["items"].append({
                        "item": item,
                        "quantity": qty,
                        "price": price,
                        "total": total
                    })

    return result