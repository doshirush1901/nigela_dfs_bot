from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Ingredient:
    item: str
    qty: float
    unit: str

@dataclass
class Dish:
    name: str
    meal_type: str
    tags: List[str]
    cook_minutes: int
    difficulty: int
    ingredients: List[Ingredient]
    steps: List[str]
    flavor_text: Optional[str] = None
    rarity: Optional[str] = "common"
    variant_adults: Optional[str] = None
    variant_kids: Optional[str] = None
    photo_bytes: Optional[bytes] = None
    public_url: Optional[str] = None
