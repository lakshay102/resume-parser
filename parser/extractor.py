# parser/extractor.py

import re
from typing import Dict, Any

# Regex patterns
EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PHONE_REGEX = r"(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}"

def extract_email(text: str) -> str:
    match = re.search(EMAIL_REGEX, text)
    return match.group() if match else ""

def extract_phone(text: str) -> str:
    match = re.search(PHONE_REGEX, text)
    return match.group() if match else ""

def extract_name(text: str) -> str:
    # Naive name guess: First non-empty line before email
    lines = text.strip().split("\n")
    for line in lines[:10]:  # Check first 10 lines
        if len(line.strip()) > 1 and not re.search(EMAIL_REGEX, line) and not re.search(PHONE_REGEX, line):
            return line.strip()
    return ""

def extract_basic_fields(text: str) -> Dict[str, Any]:
    """
    Extract basic fields from raw resume text.
    """
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
    }
