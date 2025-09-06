"""
Nutritional Analysis System for Nigela
Provides health scores, macro breakdown, and calorie contribution analysis
"""

from typing import Dict, List, Optional, Tuple
from .models import Dish, Ingredient
from .llm import _ensure_client, _client, OPENAI_MODEL_LITE
import json

# Daily calorie targets
CALORIE_TARGETS = {
    'adults_deficit': 1800,      # Parents on calorie deficit
    'adults_maintenance': 2200,   # Adults maintenance  
    'kids_growth': 1600,         # Kids immunity building
    'kids_active': 1800          # Active kids
}

# Health scoring factors
HEALTH_FACTORS = {
    'fiber_rich': 0.15,          # High fiber foods
    'protein_rich': 0.20,        # Good protein content
    'low_processed': 0.15,       # Minimal processing
    'nutrient_dense': 0.20,      # Vitamins/minerals
    'jain_friendly': 0.10,       # Dietary compliance
    'low_sugar': 0.10,           # Low added sugar
    'healthy_fats': 0.10         # Good fat sources
}

class NutritionAnalyzer:
    def __init__(self):
        self.nutrition_cache = {}
    
    def analyze_dish_nutrition(self, dish: Dish) -> Dict[str, any]:
        """Use OpenAI to analyze nutritional content of a dish"""
        
        # Check cache first
        cache_key = f"{dish.name}_{len(dish.ingredients)}"
        if cache_key in self.nutrition_cache:
            return self.nutrition_cache[cache_key]
        
        try:
            _ensure_client()
            
            # Prepare ingredients list for analysis
            ingredients_text = ", ".join([
                f"{ing.qty} {ing.unit} {ing.item}" if ing.qty > 0 
                else ing.item 
                for ing in dish.ingredients
            ])
            
            sys_prompt = """You are a nutritionist analyzing Indian vegetarian dishes. 
            Return ONLY JSON with: calories_per_serving, protein_g, carbs_g, fats_g, fiber_g, 
            health_score (0.0-1.0), health_benefits (array), dietary_notes, 
            parent_daily_percent, kids_daily_percent (assuming 1800 cal deficit adults, 1600 cal growing kids)."""
            
            user_prompt = f"""Dish: {dish.name}
Cooking time: {dish.cook_minutes} minutes
Ingredients: {ingredients_text}
Cuisine: {', '.join([t for t in dish.tags if 'cuisine:' in t])}
Cooking method: {', '.join(dish.steps[:2])}"""

            resp = _client.chat.completions.create(
                model=OPENAI_MODEL_LITE,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            nutrition_data = json.loads(resp.choices[0].message.content)
            
            # Cache the result
            self.nutrition_cache[cache_key] = nutrition_data
            
            return nutrition_data
            
        except Exception as e:
            print(f"⚠️ Nutrition analysis failed for {dish.name}: {e}")
            
            # Fallback estimation based on dish type and ingredients
            return self._estimate_nutrition_fallback(dish)
    
    def _estimate_nutrition_fallback(self, dish: Dish) -> Dict[str, any]:
        """Fallback nutrition estimation without OpenAI"""
        
        # Basic estimates based on dish type
        base_calories = 200
        
        # Adjust based on cooking method and ingredients
        if any('dal' in ing.item.lower() for ing in dish.ingredients):
            base_calories += 100  # Dal dishes higher protein
        if any('rice' in ing.item.lower() for ing in dish.ingredients):
            base_calories += 150  # Rice adds carbs
        if any('paneer' in ing.item.lower() for ing in dish.ingredients):
            base_calories += 120  # Paneer adds protein and fat
        if any('oil' in ing.item.lower() or 'ghee' in ing.item.lower() for ing in dish.ingredients):
            base_calories += 80   # Cooking fats
            
        # Calculate health score based on ingredients and tags
        health_score = 0.6  # Base score
        
        if 'jain' in dish.tags:
            health_score += 0.1
        if any('vegetable' in t or 'fruit' in t for t in dish.tags):
            health_score += 0.1
        if dish.cook_minutes <= 20:  # Quick cooking preserves nutrients
            health_score += 0.1
        if any('fried' in step.lower() for step in dish.steps):
            health_score -= 0.2
            
        health_score = min(1.0, max(0.1, health_score))  # Clamp between 0.1-1.0
        
        return {
            'calories_per_serving': base_calories,
            'protein_g': base_calories * 0.08,  # ~8% protein
            'carbs_g': base_calories * 0.55,    # ~55% carbs  
            'fats_g': base_calories * 0.25,     # ~25% fats
            'fiber_g': 5,
            'health_score': round(health_score, 1),
            'health_benefits': ['vegetarian', 'traditional'],
            'dietary_notes': 'Estimated values',
            'parent_daily_percent': round((base_calories / 1800) * 100, 1),
            'kids_daily_percent': round((base_calories / 1600) * 100, 1)
        }
    
    def get_health_score_color(self, score: float) -> str:
        """Get color for health score display"""
        if score >= 0.8:
            return '#4CAF50'  # Green - Excellent
        elif score >= 0.6:
            return '#FF9800'  # Orange - Good
        elif score >= 0.4:
            return '#FFC107'  # Yellow - Moderate
        else:
            return '#F44336'  # Red - Poor
    
    def get_health_score_label(self, score: float) -> str:
        """Get text label for health score"""
        if score >= 0.9:
            return 'EXCELLENT'
        elif score >= 0.7:
            return 'VERY GOOD'
        elif score >= 0.5:
            return 'GOOD'
        elif score >= 0.3:
            return 'MODERATE'
        else:
            return 'BASIC'

def enhance_dish_with_nutrition(dish: Dish, analyzer: NutritionAnalyzer = None) -> Dish:
    """Add nutritional information to a dish"""
    if not analyzer:
        analyzer = NutritionAnalyzer()
    
    nutrition = analyzer.analyze_dish_nutrition(dish)
    
    # Add nutrition attributes to dish
    dish.calories = nutrition.get('calories_per_serving', 200)
    dish.protein_g = nutrition.get('protein_g', 8)
    dish.carbs_g = nutrition.get('carbs_g', 30)
    dish.fats_g = nutrition.get('fats_g', 8)
    dish.fiber_g = nutrition.get('fiber_g', 5)
    dish.health_score = nutrition.get('health_score', 0.6)
    dish.health_benefits = nutrition.get('health_benefits', [])
    dish.dietary_notes = nutrition.get('dietary_notes', '')
    dish.parent_daily_percent = nutrition.get('parent_daily_percent', 10)
    dish.kids_daily_percent = nutrition.get('kids_daily_percent', 12)
    
    return dish

# Batch nutrition analysis
async def analyze_recipes_nutrition_batch(dishes: List[Dish], max_concurrent: int = 5) -> List[Dish]:
    """Analyze nutrition for multiple recipes efficiently"""
    import asyncio
    
    analyzer = NutritionAnalyzer()
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def analyze_single_dish(dish):
        async with semaphore:
            return enhance_dish_with_nutrition(dish, analyzer)
    
    # Process all dishes
    enhanced_dishes = await asyncio.gather(*[analyze_single_dish(dish) for dish in dishes])
    
    return enhanced_dishes

if __name__ == "__main__":
    # Test nutrition analysis
    from .models import Dish, Ingredient
    
    test_dish = Dish(
        name="Gujarati Dal",
        meal_type="lunch", 
        tags=["gujarati", "jain", "dal"],
        cook_minutes=30,
        difficulty=2,
        ingredients=[
            Ingredient("toor dal", 100, "g"),
            Ingredient("turmeric", 1, "tsp"),
            Ingredient("jaggery", 1, "tsp")
        ],
        steps=["Pressure cook dal", "Add tempering", "Simmer"],
        flavor_text="Comfort in every spoonful"
    )
    
    analyzer = NutritionAnalyzer()
    enhanced = enhance_dish_with_nutrition(test_dish, analyzer)
    
    print(f"✅ {enhanced.name}")
    print(f"🏥 Health Score: {enhanced.health_score}/1.0")
    print(f"🔥 Calories: {enhanced.calories}")
    print(f"👨‍👩‍👧‍👦 Parent daily %: {enhanced.parent_daily_percent}%")
    print(f"👶 Kids daily %: {enhanced.kids_daily_percent}%")
