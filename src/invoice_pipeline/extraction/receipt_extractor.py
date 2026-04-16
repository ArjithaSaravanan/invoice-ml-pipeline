import re

def extract_receipt_fields(text: str):
    result = {
        "total_amount": None,
        "items": []
    }

    total_match = re.search(r"total\s*[:\-]?\s*€?(\d+[\.,]\d*)", text, re.IGNORECASE)
    if total_match:
        result["total_amount"] = total_match.group(1)

    lines = text.splitlines()
    for line in lines:
        match = re.search(r"(.+?)\s+(\d+[\.,]?\d*)$", line)
        if match:
            item = match.group(1).strip()
            price = match.group(2)
            if len(item) > 2:
                result["items"].append({
                    "item": item,
                    "price": price
                })
                
    return result