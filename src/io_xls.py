import pandas as pd, json
from typing import List
from .models import Dish, Ingredient

def read_pantry(path: str) -> dict:
    df = pd.read_excel(path, sheet_name=0)
    stock = {}
    for _, r in df.iterrows():
        stock[str(r["ingredient"]).strip().lower()] = {
            "unit": str(r.get("unit","g")),
            "qty": float(r.get("qty_on_hand",0) or 0),
            "min_par": float(r.get("min_par",0) or 0),
        }
    return stock

def read_dishes(path: str) -> List[Dish]:
    df = pd.read_excel(path, sheet_name=0)
    dishes = []
    for _, r in df.iterrows():
        tags = r.get("tags")
        tags = json.loads(tags) if isinstance(tags, str) else (tags or [])
        ings = r.get("ingredients_json")
        ings = json.loads(ings) if isinstance(ings, str) else (ings or [])
        steps = r.get("steps_json")
        steps = json.loads(steps) if isinstance(steps, str) else (steps or [])
        dishes.append(Dish(
            name=str(r["name"]).strip(),
            meal_type=str(r["meal_type"]).strip().lower(),
            tags=[str(t).strip().lower() for t in tags],
            cook_minutes=int(r.get("cook_minutes",20)),
            difficulty=int(r.get("difficulty",2)),
            ingredients=[Ingredient(i.get("item","").lower(), float(i.get("qty",0) or 0), i.get("unit","")) for i in ings],
            steps=[str(s) for s in steps],
            flavor_text=(str(r.get("flavor_text")) if pd.notna(r.get("flavor_text")) else None),
            rarity=str(r.get("rarity","common")).lower()
        ))
    return dishes

def write_dishes(path: str, dishes: List[Dish]):
    try:
        df = pd.read_excel(path, sheet_name=0)
    except Exception:
        import pandas as pd
        df = pd.DataFrame(columns=["name","meal_type","tags","cook_minutes","difficulty","ingredients_json","steps_json","flavor_text","rarity"])
    existing = set((str(n).lower().strip(), str(m).lower().strip()) for n, m in zip(df.get("name",[]), df.get("meal_type",[])))
    rows = []
    import json as _json
    for d in dishes:
        key = (d.name.lower().strip(), d.meal_type.lower().strip())
        if key in existing: continue
        rows.append({
            "name": d.name,
            "meal_type": d.meal_type,
            "tags": _json.dumps(d.tags),
            "cook_minutes": d.cook_minutes,
            "difficulty": d.difficulty,
            "ingredients_json": _json.dumps([vars(i) for i in d.ingredients]),
            "steps_json": _json.dumps(d.steps),
            "flavor_text": d.flavor_text or "",
            "rarity": d.rarity or "common",
        })
    if rows:
        df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
        df.to_excel(path, index=False)
    return len(rows)

def read_slots(path: str) -> dict[str, list[str]]:
    df = pd.read_excel(path, sheet_name=0)
    out = {}
    for _, r in df.iterrows():
        m = str(r["meal_type"]).strip().lower()
        s = str(r["slot_name"]).strip().lower()
        out.setdefault(m, []).append(s)
    return out

def read_variants(path: str) -> dict[tuple[str,str], str]:
    df = pd.read_excel(path, sheet_name=0)
    v = {}
    for _, r in df.iterrows():
        key = (str(r["person_group"]).strip().lower(), str(r["slot_name"]).strip().lower())
        v[key] = str(r["notes"])
    return v
