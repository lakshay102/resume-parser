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
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "projects": extract_projects(text),
    }

def load_skills_list() -> set:
    """
    Hardcoded skill list. Replace or expand as needed.
    """
    return {
        "python", "java", "c++", "c#", "javascript", "typescript", "html", "css",
        "react", "angular", "vue", "node.js", "express", "next.js",
        "flutter", "dart", "swift", "kotlin",
        "sql", "mysql", "postgresql", "mongodb", "firebase",
        "docker", "kubernetes", "aws", "azure", "gcp",
        "git", "github", "jira", "linux", "bash",
        "fastapi", "django", "flask", "rest api", "graphql",
        "pandas", "numpy", "matplotlib", "tensorflow", "pytorch", "sklearn",
        "excel", "power bi", "tableau", "figma", "corel draw", "after effects", "photoshop", "premiere pro"
    }

def extract_skills(text: str) -> list:
    skills_found = set()
    skills_list = load_skills_list()
    lowered_text = text.lower()
    
    for skill in skills_list:
        if skill.lower() in lowered_text:
            skills_found.add(skill.lower())
    
    return sorted(skills_found)

SECTION_HEADERS = [
    "education",
    "work experience",
    "experience",
    "professional experience",
    "projects",
    "academic projects",
    "personal projects",
    "internship",
]

def extract_sections(text: str) -> Dict[str, str]:
    """
    Extracts major sections like education, experience, and projects
    by locating their headers in the resume.
    """
    lines = text.splitlines()
    sections = {}
    current_section = None
    buffer = []

    for line in lines:
        line_clean = line.strip().lower()

        # Detect section header
        matched_header = next((h for h in SECTION_HEADERS if h in line_clean), None)
        if matched_header:
            # Save previous section
            if current_section and buffer:
                sections[current_section] = "\n".join(buffer).strip()
                buffer.clear()
            current_section = matched_header
        elif current_section:
            buffer.append(line)

    # Add last captured section
    if current_section and buffer:
        sections[current_section] = "\n".join(buffer).strip()

    return sections


def extract_education(text: str) -> str:
    sections = extract_sections(text)
    for key in sections:
        if "education" in key:
            return sections[key]
    return ""

def extract_experience(text: str) -> str:
    sections = extract_sections(text)
    for key in sections:
        if "experience" in key or "internship" in key:
            return sections[key]
    return ""

def extract_projects(text: str) -> str:
    sections = extract_sections(text)
    for key in sections:
        if "project" in key:
            return sections[key]
    return ""
