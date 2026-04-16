import re

def clean_text(text: str) -> str:
    """
    Remove unwanted characters and normalize text.
    """
    text = re.sub(r'[^\w\s€.-]', '', text)  # Keep only alphanumeric, whitespace, and some punctuation
    return text.strip()

def clean_number(value: str):
    """
    Convert extracted string to integer safely.
    """
    value = re.sub(r'[^\d]', '', value)  # Remove non-digit characters
    return int(value) if value else None