import json, re
from pathlib import Path
from typing import Optional, List
from .parse_pdf import pdf_to_text
from .normalize import text_to_dishes
from .io_xls import write_dishes
from .llm import parse_recipe_block_batch, classify_titles, to_dishes, embed_for_dedup

CUISINE_HINTS = {
    "gujarati":["gujarat","gujarati","kathiawar","surati"],
    "rajasthani":["rajasthan","rajasthani","marwari"],
    "himachali":["himachal","pahadi","kangra"],
    "kerala":["kerala","malabar","kannur","trivandrum","travancore"],
    "tamil":["tamil","tamil nadu","chettinad","tiffin"],
    "goan":["goa","goan"],
    "south":["south indian","udupi","mangalore","karnataka","andhra","telugu","kerala","tamil"],
    "north":["north indian","punjab","punjabi","delhi","awadh","lucknow"],
    "italian":["italian","pasta","pizza"],
    "mexican":["mexican","taco","enchilada","quesadilla"],
    "japanese":["japanese","ramen","sushi","miso"],
    "burmese":["burmese","myanmar","khow suey","ohn no khao swe"],
    "indian chinese":["indo chinese","indian chinese","hakka","schezwan"],
}

def infer_cuisine(title: str) -> Optional[str]:
    t = (title or "").lower()
    for k,hints in CUISINE_HINTS.items():
        if any(h in t for h in hints): return k
    return None

def ingest_manifest_to_dishes(manifest_path: str, data_dir="data", meal_hint_default="dinner",
                              max_books: int = 20, max_lines: Optional[int] = 12000) -> int:
    mpath = Path(manifest_path)
    if not mpath.exists():
        print(f"Manifest not found: {manifest_path}")
        return 0
    books = json.loads(mpath.read_text())[:max_books]

    # 1) Extract text chunks
    raw_blocks = []
    meta = []
    for b in books:
        pdf_path = b.get("path"); title = b.get("title") or ""
        if not pdf_path or not Path(pdf_path).exists(): continue
        cuisine_hint = infer_cuisine(title)
        raw = pdf_to_text(pdf_path)
        if max_lines: raw = "\n".join(raw.splitlines()[:max_lines])
        # chunk on blank lines, keep only 200–2500 char blocks
        for ch in [c.strip() for c in raw.split("\n\n") if c.strip()]:
            if 200 <= len(ch) <= 2500:
                raw_blocks.append(ch); meta.append({"title": title, "cuisine_hint": cuisine_hint})

    # 2) Structured parse with OpenAI (JSON schema; Jain/veg enforced)
    parsed = parse_recipe_block_batch(raw_blocks, meal_hint_default, [m["cuisine_hint"] for m in meta])

    # 3) If any items have only title-like strings, run classifier
    titles = [p.get("name","") for p in parsed]
    classes = classify_titles(titles)

    # 4) Convert to Dish dataclasses (+ tag slots, substitutes), then de-dup via embeddings
    dishes = to_dishes(parsed, classes)
    dishes = embed_for_dedup(dishes)

    # 5) Write to Excel
    return write_dishes(Path(data_dir) / "dishes.xlsx", dishes)
