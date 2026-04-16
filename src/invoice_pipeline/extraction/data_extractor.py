import re
from typing import Optional, Dict
from invoice_pipeline.extraction.cleaner import clean_text, clean_number
from invoice_pipeline.extraction.field_aliases import FIELD_ALIASES

def _build_label_pattern(alias_list):
    escaped_aliases = [re.escape(alias) for alias in alias_list]
    return r"(?:%s)" % "|".join(escaped_aliases)

def _extract_field_by_alias(text: str, field_name: str) -> Optional[str]:
    aliases = FIELD_ALIASES[field_name]["aliases"]
    label_pattern = _build_label_pattern(aliases)

    pattern = rf"(?i){label_pattern}\s*[:#-]?\s*(.+)"
    for line in text.splitlines():
        line = line.strip()
        match = re.search(pattern, line)
        if match:
            value = match.group(1).strip()
            value = re.split(r"\s{2,}", value)[0].strip()
            return value
    return None


def extract_invoice_fields(text: str) -> Dict:
    """
    Extract structured invoice fields from the OCR text
    """
    result = {
        "invoice_number": None,
        "date": None,
        "due_date": None,
        "total_amount": None,
        "items": []
    }

    result["invoice_number"] = _extract_field_by_alias(text, "invoice_number")
    result["date"] = _extract_field_by_alias(text, "date")
    result["due_date"] = _extract_field_by_alias(text, "due_date")

    total_raw = _extract_field_by_alias(text, "total_amount")
    if total_raw:
        total_match = re.search(r"(\d+[.,]?\d*)", total_raw)
        if total_match:
            result["total_amount"] = total_match.group(1).replace(",", ".")

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        if "|" in line:
            parts = [clean_text(p) for p in line.split("|") if p.strip()]

            if len(parts) >= 4:
                item = clean_text(parts[0])
                qty = clean_number(parts[1])
                price = clean_number(parts[2])
                total = clean_number(parts[3])

                if item and qty is not None and price is not None:
                    result["items"].append({
                        "item": item,
                        "quantity": qty,
                        "price": price,
                        "total": total
                    })
    return result