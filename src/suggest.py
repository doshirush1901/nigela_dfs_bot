from datetime import date
from typing import Dict, List, Optional, Union
from .io_xls import read_pantry, read_dishes, read_slots, read_variants
from .scoring import score
from .models import Dish

def pick_for_slot(cands: List[Dish], stock: Dict, used_last: set[str]) -> Optional[Dish]:
    if not cands: return None
    ranked = sorted(cands, key=lambda d: score(d, stock, used_last), reverse=True)
    return ranked[0] if ranked else None

def suggest_for_day(day: date, data_dir="data") -> dict:
    stock = read_pantry(f"{data_dir}/pantry.xlsx")
    dishes = read_dishes(f"{data_dir}/dishes.xlsx")
    slots = read_slots(f"{data_dir}/slots.xlsx")
    variants = read_variants(f"{data_dir}/variants.xlsx")

    # Enhanced 5-meal plan structure
    meal_structure = {
        'breakfast': ['main_starch', 'protein', 'yogurt', 'fruit'],
        'morning_snack': ['fruit', 'nuts', 'beverage'],
        'lunch': ['salad', 'dal', 'rice', 'roti', 'vegetable', 'farsan'],
        'evening_snack': ['farsan', 'tea', 'light_bite'],
        'dinner': ['soup', 'khichdi', 'bread', 'vegetable_west', 'protein_farsan', 'digestif']
    }

    out = {}
    used_names = set()
    
    for meal, slot_list in meal_structure.items():
        out[meal] = {}
        for slot in slot_list:
            # Look for dishes with appropriate tags
            cands = [d for d in dishes if any(t == f"{meal.replace('_snack', '')}:{slot}" for t in d.tags)]
            
            # If no specific matches, broaden search
            if not cands and meal.endswith('_snack'):
                cands = [d for d in dishes if any(slot in t for t in d.tags)]
            
            pick = pick_for_slot(cands, stock, used_names)
            if pick:
                used_names.add(pick.name.lower())
                pick.variant_adults = variants.get(("adult", slot))
                pick.variant_kids   = variants.get(("kids", slot))
                out[meal][slot] = pick
    
    return out
