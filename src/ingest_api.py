import httpx
from typing import List
from .models import Dish, Ingredient
from .config import SPOONACULAR_API_KEY, EDAMAM_APP_ID, EDAMAM_APP_KEY
from .normalize import guess_tags

async def spoonacular_search(query: str, number: int = 5):
    if not SPOONACULAR_API_KEY: return []
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {"apiKey": SPOONACULAR_API_KEY, "query": query, "diet":"vegetarian", "number": number, "addRecipeInformation": True}
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.get(url, params=params); r.raise_for_status()
        return r.json().get("results", [])

async def edamam_search(query: str, number: int = 5):
    if not (EDAMAM_APP_ID and EDAMAM_APP_KEY): return []
    url = "https://api.edamam.com/api/recipes/v2"
    params = {"type":"public","q":query,"app_id":EDAMAM_APP_ID,"app_key":EDAMAM_APP_KEY,"health":["vegetarian"],"random":"true"}
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.get(url, params=params); r.raise_for_status()
        hits = r.json().get("hits", [])
        return [h.get("recipe",{}) for h in hits][:number]

def map_spoonacular(items, meal_hint=None, cuisine_hint=None) -> List[Dish]:
    out=[]
    for it in items or []:
        name = (it.get("title") or "").strip()
        if not name: continue
        tags = guess_tags(name, meal_hint, cuisine_hint)
        ings = [Ingredient(i.get("name","").lower(), float(i.get("amount") or 0), i.get("unit","")) for i in (it.get("extendedIngredients") or [])]
        steps = []
        ai = (it.get("analyzedInstructions") or [])
        if ai and ai[0].get("steps"): steps = [s.get("step","") for s in ai[0]["steps"]]
        out.append(Dish(
            name=name, meal_type=(meal_hint or "dinner"), tags=tags,
            cook_minutes=int(it.get("readyInMinutes") or 20), difficulty=2,
            ingredients=ings or [Ingredient("salt",1,"tsp")], steps=steps or ["Follow recipe link"],
            flavor_text="API import", rarity="common", public_url=it.get("sourceUrl")
        ))
    return out

def map_edamam(items, meal_hint=None, cuisine_hint=None) -> List[Dish]:
    out=[]
    for it in items or []:
        name = (it.get("label") or "").strip()
        if not name: continue
        tags = guess_tags(name, meal_hint, cuisine_hint)
        ings = [Ingredient(str(x), 0, "") for x in (it.get("ingredientLines") or [])]
        out.append(Dish(
            name=name, meal_type=(meal_hint or "dinner"), tags=tags,
            cook_minutes=20, difficulty=2,
            ingredients=ings or [Ingredient("salt",1,"tsp")], steps=["Open link for steps"],
            flavor_text="API import", rarity="common", public_url=it.get("url")
        ))
    return out
