import pdfplumber
from .normalize import text_to_dishes

def pdf_to_text(path: str) -> str:
    parts=[]
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            t = p.extract_text() or ""
            if t.strip(): parts.append(t)
    return "\n".join(parts)

def pdf_to_dishes(path: str, meal_hint=None, cuisine_hint=None):
    return text_to_dishes(pdf_to_text(path), meal_hint, cuisine_hint)
