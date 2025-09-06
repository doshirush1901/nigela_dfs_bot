import pytesseract
from PIL import Image
from .normalize import text_to_dishes

def image_to_text(path: str) -> str:
    try:
        im = Image.open(path)
        return pytesseract.image_to_string(im)
    except Exception:
        return ""

def image_to_dishes(path: str, cuisine_hint=None):
    txt = image_to_text(path)
    return text_to_dishes(txt, meal_hint=None, cuisine_hint=cuisine_hint)
