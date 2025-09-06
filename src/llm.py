import os, json, math, hashlib
from typing import List, Dict, Any, Optional
from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_MODEL_MAIN, OPENAI_MODEL_LITE, OPENAI_EMBED_MODEL
from .models import Dish, Ingredient

_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# ---------- A) Structured parser (JSON schema) ----------
_SCHEMA = {
  "type":"object",
  "properties":{
    "name":{"type":"string"},
    "meal_type":{"type":"string","enum":["breakfast","lunch","dinner","snack_am","snack_pm"]},
    "cuisine":{"type":"string"},
    "tags":{"type":"array","items":{"type":"string"}},
    "cook_minutes":{"type":"integer"},
    "difficulty":{"type":"integer","minimum":1,"maximum":5},
    "ingredients":{"type":"array","items":{
      "type":"object",
      "properties":{"item":{"type":"string"},"qty":{"type":"number"},"unit":{"type":"string"}},
      "required":["item","qty","unit"],"additionalProperties":False
    }},
    "steps":{"type":"array","items":{"type":"string"}},
    "notes":{"type":"string"},
    "jain_ok":{"type":"boolean"},
    "substitutions":{"type":"array","items":{"type":"string"}}
  },
  "required":["name","meal_type","cuisine","tags","cook_minutes","difficulty","ingredients","steps","notes","jain_ok","substitutions"],
  "additionalProperties": False
}

def _ensure_client():
    if not _client:
        raise RuntimeError("OPENAI_API_KEY missing; set it in .env")

def parse_recipe_block(raw_text: str, meal_hint: Optional[str]=None, cuisine_hint: Optional[str]=None) -> Dict[str,Any]:
    _ensure_client()
    sys = ("You are Nigela, a vegetarian/Jain chef-assistant. "
           "Return ONLY JSON matching the provided schema. If a dish violates Jain/vegetarian/eggless, "
           "provide Jain-compliant substitutions and set jain_ok=false; otherwise true.")
    user = f"Meal hint: {meal_hint or 'none'} | Cuisine hint: {cuisine_hint or 'none'}\n\n{raw_text}"
    resp = _client.chat.completions.create(
        model=OPENAI_MODEL_MAIN,
        messages=[{"role":"system","content":sys},{"role":"user","content":user}],
        response_format={"type":"json_schema","json_schema":{"name":"dish","strict":True,"schema":_SCHEMA}},
        temperature=0.2
    )
    return json.loads(resp.choices[0].message.content)

def parse_recipe_block_batch(blocks: List[str], meal_hint: Optional[str], cuisines: List[Optional[str]]) -> List[Dict[str,Any]]:
    # small helper that runs one-by-one to keep memory low; swap to Batch API for huge sets
    out=[]
    for i, b in enumerate(blocks):
        try:
            out.append(parse_recipe_block(b, meal_hint, cuisines[i] if i < len(cuisines) else None))
        except Exception:
            continue
    return out

# ---------- B) Title classifier ----------
def classify_titles(titles: List[str]) -> List[Dict[str,str]]:
    if not titles: return []
    _ensure_client()
    sys = ("Return a compact JSON array. For each title, detect {title, meal_type(one of breakfast/lunch/dinner/snack_am/snack_pm), "
           "slot(one of main_starch, protein, yogurt, fruit, salad, dal, rice, roti, vegetable, farsan, soup, khichdi, bread, vegetable_west, protein_farsan, digestif), "
           "cuisine, jain_ok:true/false}. Use Indian home-cooking knowledge.")
    user = "Titles:\n" + "\n".join(f"- {t}" for t in titles)
    resp = _client.chat.completions.create(
        model=OPENAI_MODEL_LITE,
        messages=[{"role":"system","content":sys},{"role":"user","content":user}],
        response_format={"type":"json_object"},
        temperature=0.1
    )
    data = json.loads(resp.choices[0].message.content)
    if isinstance(data, dict) and "items" in data:
        return data["items"]
    if isinstance(data, list):
        return data
    # best-effort fallback
    return [{"title": t, "meal_type":"dinner","slot":"vegetable","cuisine":"indian","jain_ok":True} for t in titles]

# ---------- C) Email copy in Nigela's voice ----------
def nightly_email_copy(plan: Dict[str, Dict[str, Any]]) -> str:
    _ensure_client()
    sys = ("You are Nigela, warm and practical. Write a beautiful email for a complete 5-meal day plan "
           "(breakfast, morning snack, lunch, evening snack, dinner). Include cooking timeline and loving notes. "
           "Keep it Jain/vegetarian, family-friendly. Use Indian-English warmth.")
    
    # Convert plan to serializable format
    serializable_plan = {}
    for meal, slots in plan.items():
        serializable_plan[meal] = {}
        for slot, dish in slots.items():
            serializable_plan[meal][slot] = {
                "name": dish.name,
                "cook_minutes": dish.cook_minutes,
                "difficulty": dish.difficulty,
                "tags": dish.tags,
                "flavor_text": dish.flavor_text
            }
    
    user = f"Complete 5-meal plan JSON:\n{json.dumps(serializable_plan, ensure_ascii=False)}"
    resp = _client.chat.completions.create(model=OPENAI_MODEL_LITE, messages=[{"role":"system","content":sys},{"role":"user","content":user}], temperature=0.6)
    return resp.choices[0].message.content

# ---------- D) Embeddings & de-dup ----------
def _emb(texts: List[str]) -> List[List[float]]:
    _ensure_client()
    r = _client.embeddings.create(model=OPENAI_EMBED_MODEL, input=texts)
    return [d.embedding for d in r.data]

def _cos(a: List[float], b: List[float]) -> float:
    import math
    dot = sum(x*y for x,y in zip(a,b))
    na = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(x*x for x in b))
    return dot / (na*nb + 1e-9)

def embed_for_dedup(dishes: List[Dish], threshold: float = 0.92) -> List[Dish]:
    if len(dishes) < 2 or not OPENAI_API_KEY:
        return dishes
    payload = [f"{d.name} :: " + ", ".join(sorted(set(i.item for i in d.ingredients if i.item))) for d in dishes]
    embs = _emb(payload)
    keep = []
    for i, di in enumerate(dishes):
        dup = False
        for j in range(len(keep)):
            if _cos(embs[i], embs[keep[j][0]]) > threshold:
                dup = True; break
        if not dup:
            keep.append((i, di))
    return [di for _, di in keep]

# ---------- E) Map parsed JSON -> Dish dataclasses ----------
def to_dishes(parsed: List[Dict[str,Any]], classes: List[Dict[str,str]]) -> List[Dish]:
    by_title = { (c.get("title") or "").lower(): c for c in (classes or []) }
    out=[]
    for p in parsed:
        name = p.get("name","").strip()
        if not name: continue
        title_key = name.lower()
        # merge classifier hints
        meal_type = (p.get("meal_type") or (by_title.get(title_key,{}).get("meal_type"))) or "dinner"
        slot = by_title.get(title_key,{}).get("slot")
        cuisine = p.get("cuisine") or by_title.get(title_key,{}).get("cuisine")
        tags = list({*(p.get("tags") or []), "vegetarian", "jain"})
        if cuisine: tags.append(f"cuisine:{cuisine.lower()}")
        if slot: tags.append(f"{meal_type}:{slot}")
        steps = p.get("steps") or ["Follow recipe steps."]
        ings = [Ingredient(i.get("item","").lower(), float(i.get("qty") or 0), i.get("unit","")) for i in (p.get("ingredients") or [])]
        out.append(Dish(
            name=name, meal_type=meal_type, tags=tags,
            cook_minutes=int(p.get("cook_minutes") or 20),
            difficulty=int(p.get("difficulty") or 2),
            ingredients=ings or [Ingredient("salt",1,"tsp")],
            steps=steps, flavor_text=p.get("notes") or "Nigela note: bloom spices gently.",
            rarity="common", public_url=None
        ))
    return out
