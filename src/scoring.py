from .models import Dish
from typing import Dict

def pantry_ok(d: Dish, stock: Dict[str, dict]) -> bool:
    for i in d.ingredients:
        if not i.item: continue
        have = stock.get(i.item.lower(), {"qty":0})["qty"]
        if have < (i.qty or 0): return False
    return True

def score(d: Dish, stock: Dict[str, dict], used_last: set[str]) -> float:
    s = 0.0
    if not pantry_ok(d, stock): return -999
    tags = set(d.tags or [])
    if "jain" in tags: s += 10
    if any(t.startswith("cuisine:") for t in tags): s += 2
    if d.name.lower() in used_last: s -= 100
    if d.cook_minutes <= 25: s += 3
    if "kid-friendly" in tags: s += 2
    return s
