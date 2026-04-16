def detect_document_type(text: str) -> str:
    text_lower = text.lower()
    if "invoice number" in text_lower:
        return "invoice"
    if "total amount" in text_lower:
        return "invoice"
    if "tax invoice" in text_lower:
        return "enterprise_invoice"
    if "subtotal" in text_lower or "tax" in text_lower:
        return "receipt"
    if "total" in text_lower:
        return "receipt"
    return "unknown"
