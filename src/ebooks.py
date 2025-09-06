import os, json, re, asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
import httpx
from bs4 import BeautifulSoup

IA_ADV_URL = "https://archive.org/advancedsearch.php"
IA_META_URL = "https://archive.org/metadata/"
COMMONS_API  = "https://commons.wikimedia.org/w/api.php"

DEFAULT_CUISINES = ["gujarati","rajasthani","himachali","kerala","tamil","goan","italian","mexican","japanese","burmese","indian chinese","south indian","north indian"]
DEFAULT_DIET_TERMS = ["jain","vegetarian","veg","meatless","eggless","satvik","sattvic"]

def _uniq(seq):
    seen=set(); out=[]
    for x in seq:
        # Use URL as unique key for dict items
        key = x.get("url") if isinstance(x, dict) else x
        if key not in seen:
            seen.add(key); out.append(x)
    return out

def build_queries(cuisines=None, diet_terms=None):
    cuisines = cuisines or DEFAULT_CUISINES
    diet_terms = diet_terms or DEFAULT_DIET_TERMS
    diet_q = " OR ".join([f'"{t}"' for t in diet_terms])
    topic_q = '("cookbook" OR "cook book" OR "recipes" OR "cookery")'
    base   = f'({topic_q}) AND mediatype:texts AND (licenseurl:* OR rights:*)'
    qs=[]
    for c in cuisines:
        qs.append(f'{base} AND (subject:("{c}") OR title:("{c}") OR description:("{c}"))')
    qs += [
        f'{base} AND (subject:(vegetarian) OR title:(vegetarian) OR subject:(meatless))',
        f'{base} AND (subject:({diet_q}) OR title:({diet_q}))',
        f'{base} AND (subject:(indian vegetarian) OR title:(indian vegetarian))'
    ]
    return _uniq(qs)

async def ia_search(session: httpx.AsyncClient, query: str, rows: int = 10):
    params = {"q": query, "fl[]":["identifier","title","year","language","licenseurl","rights","downloads"], "sort[]":"downloads desc", "rows":rows, "output":"json", "page":1}
    r = await session.get(IA_ADV_URL, params=params); r.raise_for_status()
    data = r.json()
    return data.get("response", {}).get("docs", [])

async def ia_choose_pdf(session: httpx.AsyncClient, identifier: str) -> Optional[Dict[str,str]]:
    r = await session.get(IA_META_URL + identifier); r.raise_for_status()
    files = (r.json().get("files") or [])
    pdfs = [f for f in files if ("pdf" in (f.get("format","").lower())) or str(f.get("name","")).lower().endswith(".pdf")]
    if not pdfs: return None
    pdfs.sort(key=lambda f: int(f.get("size",0) or 0), reverse=True)
    top = pdfs[0]
    return {"url": f'https://archive.org/download/{identifier}/{top.get("name")}', "name": top.get("name") or f"{identifier}.pdf"}

def ia_is_open(doc):
    lic = (doc.get("licenseurl") or "").lower()
    rights = (doc.get("rights") or "").lower()
    if "creativecommons" in lic: return True
    if "public domain" in rights or "public-domain" in rights: return True
    try:
        y = int(str(doc.get("year","")).split()[0][:4])
        if y and y <= 1929: return True
    except Exception:
        pass
    return False

async def commons_list_pdfs(session: httpx.AsyncClient, category="Vegetarian cookbooks", limit=40):
    params = {"action":"query","list":"categorymembers","cmtitle":f"Category:{category.replace(' ','_')}",
              "cmnamespace":"6","cmlimit":min(limit,500),"format":"json"}
    r = await session.get(COMMONS_API, params=params); r.raise_for_status()
    members = r.json().get("query",{}).get("categorymembers",[]) or []
    titles = [m["title"] for m in members if m.get("title","").startswith("File:")]
    if not titles: return []
    params2 = {"action":"query","prop":"imageinfo","iiprop":"url","format":"json","titles":"|".join(titles[:50])}
    r2 = await session.get(COMMONS_API, params=params2); r2.raise_for_status()
    pages = r2.json().get("query",{}).get("pages",{}) or {}
    out=[]
    for _,p in pages.items():
        i = (p.get("imageinfo") or [None])[0]
        if not i: continue
        url = i.get("url")
        if url and url.lower().endswith(".pdf"):
            out.append({"title": p.get("title","").replace("File:",""), "url": url})
    return out

VITALITA_PAGES = [
    "https://www.vitalita.com/vcg/cookbooks/a_taste_of_vitality_book.html",
    "https://vitalita.com/vcg/cookbooks/desserts_of_vitality_book.html",
]

async def vitalita_find_pdfs(session: httpx.AsyncClient):
    out=[]
    for page in VITALITA_PAGES:
        r = await session.get(page, follow_redirects=True, timeout=20.0); r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        for a in soup.select("a[href]"):
            href = a["href"]
            if href.lower().endswith(".pdf"):
                url = href if href.startswith("http") else page.rsplit("/",1)[0] + "/" + href
                title = "Vitalita — " + (a.get_text(strip=True) or "Cookbook PDF")
                out.append({"title": title, "url": url})
    return out

async def discover_free_cookbooks(preferences: Dict[str, Any], max_total: int = 20):
    cuisines = preferences.get("cuisines") or DEFAULT_CUISINES
    diet_terms = preferences.get("diet_terms") or DEFAULT_DIET_TERMS
    async with httpx.AsyncClient(timeout=20.0, follow_redirects=True, headers={"User-Agent":"Nigela/ebooks"}) as s:
        commons = await commons_list_pdfs(s, "Vegetarian cookbooks", 40)
        vit = await vitalita_find_pdfs(s)
        docs=[]
        for q in build_queries(cuisines, diet_terms)[:8]:
            try:
                docs.extend(await ia_search(s, q, rows=8))
            except Exception:
                pass
        ia_candidates=[]
        for d in docs:
            if not ia_is_open(d): continue
            ident = d.get("identifier"); title = d.get("title") or ident
            if not ident: continue
            pdf = await ia_choose_pdf(s, ident)
            if not pdf: continue
            ia_candidates.append({"title": title, "url": pdf["url"], "source":"IA", "identifier": ident, "license": d.get("licenseurl") or d.get("rights")})
        pool = _uniq(ia_candidates + commons + vit)
        return pool[:max_total]

async def download_files(items, out_dir: str):
    outp = Path(out_dir); outp.mkdir(parents=True, exist_ok=True)
    results=[]
    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as s:
        for it in items:
            url = it["url"]
            safe = re.sub(r"[^A-Za-z0-9._-]+","_", (it.get("title") or it.get("identifier") or "cookbook"))[:80] + ".pdf"
            dest = outp / safe
            if dest.exists():
                results.append({**it, "path": str(dest)}); continue
            try:
                r = await s.get(url); r.raise_for_status()
                dest.write_bytes(r.content)
                results.append({**it, "path": str(dest)})
            except Exception:
                continue
    man = outp / "manifest.json"
    existing = []
    if man.exists():
        try: existing = json.loads(man.read_text())
        except Exception: existing = []
    merged = existing + [x for x in results if x not in existing]
    man.write_text(json.dumps(merged, indent=2))
    return results

def fetch_ebooks(preferences, out_dir="library/ebooks", max_total=20):
    import asyncio
    items = asyncio.run(discover_free_cookbooks(preferences, max_total=max_total))
    return asyncio.run(download_files(items, out_dir))
