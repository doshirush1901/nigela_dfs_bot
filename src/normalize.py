import re
from typing import List, Optional
from .models import Dish, Ingredient

DISH_LINE = re.compile(r"^\s*(?:-|\u2022|\*)?\s*([A-Za-z0-9 ()/&,+.'-]{3,80})\s*$", re.I)

SLOT_KEYWORDS = {
  "breakfast:main_starch": ["dosa","idli","paratha","thepla","pancake","upma","poha"],
  "breakfast:protein": ["moong","sprout","paneer","chilla","dal pancake"],
  "breakfast:yogurt": ["curd","yogurt","lassi"],
  "breakfast:fruit": ["banana","papaya","mango","fruit","orange"],
  "lunch:salad": ["salad","kachumber"],
  "lunch:dal": ["dal","kadhi","sambar","rasam"],
  "lunch:rice": ["rice","pulao","biryani","quinoa"],
  "lunch:roti": ["roti","phulka","chapati","thepla","bhakri"],
  "lunch:vegetable": ["sabzi","bhindi","aloo","baingan","gobi","beans"],
  "lunch:farsan": ["dhokla","khaman","patra","sev","farsan"],
  "dinner:soup": ["soup","broth","ramen"],
  "dinner:khichdi": ["khichdi","kichdi","risotto"],
  "dinner:bread": ["paratha","bhakri","dosa","thepla","naan"],
  "dinner:vegetable_west": ["broccoli","zucchini","stir-fry","bake","grill"],
  "dinner:protein_farsan": ["tikki","muthiya","paneer","tofu"],
  "dinner:digestif": ["ajwain","fennel","saunf","haritaki"],
}

def guess_tags(name: str, meal_hint: Optional[str] = None, cuisine_hint: Optional[str] = None) -> List[str]:
    low = (name or "").lower()
    tags = ["jain","vegetarian"]
    if cuisine_hint:
        tags.append(f"cuisine:{cuisine_hint.lower()}")
    for slot, kws in SLOT_KEYWORDS.items():
        if any(k in low for k in kws):
            tags.append(slot)
    if meal_hint and all(not t.startswith(meal_hint) for t in tags):
        tags.append(f"{meal_hint}:misc")
    return list(dict.fromkeys(tags))

def text_to_dishes(raw_text: str, meal_hint: Optional[str] = None, cuisine_hint: Optional[str] = None) -> List[Dish]:
    lines = [l.strip() for l in (raw_text or "").splitlines() if l.strip()]
    out = []
    for l in lines:
        m = DISH_LINE.match(l)
        if not m: continue
        name = m.group(1)
        tags = guess_tags(name, meal_hint, cuisine_hint)
        meal_type = (meal_hint or (tags[0].split(":")[0] if ":" in tags[0] else "dinner")).split(":")[0]
        out.append(Dish(
            name=name,
            meal_type=meal_type,
            tags=tags, cook_minutes=20, difficulty=2,
            ingredients=[Ingredient("salt", 1, "tsp")],
            steps=["Prep ingredients","Cook to taste"],
            flavor_text="Nigela whispers: keep it gentle.",
            rarity="common"
        ))
    return out
