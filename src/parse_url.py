import httpx
from bs4 import BeautifulSoup
from readability import Document
from .normalize import text_to_dishes

async def extract_text_from_url(url: str) -> str:
    async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
        r = await client.get(url); r.raise_for_status()
        html = r.text
    try:
        doc = Document(html); content_html = doc.summary()
        soup = BeautifulSoup(content_html, "lxml")
        return soup.get_text("\n", strip=True)
    except Exception:
        soup = BeautifulSoup(html, "lxml")
        return soup.get_text("\n", strip=True)

async def url_to_dishes(url: str, meal_hint=None, cuisine_hint=None):
    txt = await extract_text_from_url(url)
    return text_to_dishes(txt, meal_hint, cuisine_hint)
