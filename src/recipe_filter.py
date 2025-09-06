"""
Smart Recipe Card Filtering
Only shows recipe cards for dishes that need actual cooking instructions
"""

def needs_recipe_card(dish) -> bool:
    """Determine if a dish needs a detailed recipe card"""
    
    # Simple items that don't need recipe cards
    simple_keywords = [
        'slice', 'slices', 'bowl', 'fresh', 'cut', 'chopped',
        'raw', 'plain', 'simple', 'basic'
    ]
    
    # Very simple preparation methods
    simple_methods = [
        'slice', 'cut', 'chop', 'arrange', 'serve', 'mix and serve'
    ]
    
    dish_name = dish.name.lower()
    
    # Check if dish name contains simple keywords
    if any(keyword in dish_name for keyword in simple_keywords):
        return False
    
    # Check cooking time - very quick items usually don't need cards
    if dish.cook_minutes <= 5:
        # But some quick items still need cards (like tempering, spice mixes)
        if any(word in dish_name for word in ['tadka', 'tempering', 'masala', 'spice']):
            return True
        return False
    
    # Check if steps are very simple
    steps = getattr(dish, 'steps', [])
    if len(steps) <= 2:
        # Check if steps are basic
        steps_text = ' '.join(steps).lower()
        if any(simple_method in steps_text for simple_method in simple_methods):
            return False
    
    # Check ingredients - if very few and simple, might not need card
    ingredients = getattr(dish, 'ingredients', [])
    if len(ingredients) <= 2:
        ingredient_names = [getattr(ing, 'item', '').lower() for ing in ingredients]
        if all(ing in ['salt', 'water', 'lemon', 'honey', 'sugar'] for ing in ingredient_names):
            return False
    
    # Check difficulty level
    if getattr(dish, 'difficulty', 2) <= 1 and dish.cook_minutes <= 10:
        # Very easy and quick - might be too simple
        if any(word in dish_name for word in ['fruit', 'banana', 'slice', 'cut']):
            return False
    
    # Default: show recipe card for anything else
    return True

def filter_dishes_for_cards(plan: dict) -> dict:
    """Filter meal plan to only include dishes that need recipe cards"""
    
    filtered_plan = {}
    
    for meal_name, dishes in plan.items():
        filtered_dishes = {}
        
        for slot_name, dish in dishes.items():
            if needs_recipe_card(dish):
                filtered_dishes[slot_name] = dish
        
        if filtered_dishes:  # Only include meal if it has dishes needing cards
            filtered_plan[meal_name] = filtered_dishes
    
    return filtered_plan

def get_simple_items_summary(plan: dict) -> dict:
    """Get summary of simple items that don't need recipe cards"""
    
    simple_items = {}
    
    for meal_name, dishes in plan.items():
        simple_list = []
        
        for slot_name, dish in dishes.items():
            if not needs_recipe_card(dish):
                simple_list.append(dish.name)
        
        if simple_list:
            simple_items[meal_name] = simple_list
    
    return simple_items

def generate_optimized_meal_overview(plan: dict) -> str:
    """Generate overview table highlighting which items have recipe cards"""
    
    # Separate complex and simple items
    complex_items = filter_dishes_for_cards(plan)
    simple_items = get_simple_items_summary(plan)
    
    table_html = """
    <div style="
        background: white;
        border-radius: 8px;
        margin-bottom: 32px;
        border: 1px solid #000000;
    ">
        <div style="
            background: #000000;
            color: white;
            padding: 16px;
            text-align: center;
        ">
            <h2 style="
                margin: 0;
                font-size: 16px;
                font-weight: 500;
                letter-spacing: 1px;
            ">TODAY'S MENU</h2>
        </div>
        
        <div style="padding: 16px;">
    """
    
    meal_emojis = {
        'breakfast': '🌅',
        'morning_snack': '🥝',
        'lunch': '☀️',
        'evening_snack': '☕',
        'dinner': '🌙'
    }
    
    # Generate meal sections
    for meal_key, dishes in plan.items():
        meal_name = meal_key.replace('_', ' ').title()
        emoji = meal_emojis.get(meal_key, '🍽️')
        
        # Count complex vs simple items
        complex_count = len(complex_items.get(meal_key, {}))
        simple_count = len(simple_items.get(meal_key, []))
        
        all_items = []
        
        # Add complex items (with card indicator)
        for dish in complex_items.get(meal_key, {}).values():
            all_items.append(f"<strong>{dish.name}</strong> 📋")
        
        # Add simple items (no card needed)
        for item_name in simple_items.get(meal_key, []):
            all_items.append(f"{item_name}")
        
        items_text = ' • '.join(all_items) if all_items else 'No items planned'
        
        table_html += f"""
        <div style="
            display: flex;
            padding: 12px 0;
            border-bottom: 1px solid #e0e0e0;
            font-size: 13px;
        ">
            <div style="
                flex: 1;
                font-weight: 600;
                color: #000;
                padding-right: 12px;
            ">{emoji} {meal_name}</div>
            <div style="
                flex: 2;
                color: #666;
                line-height: 1.4;
            ">{items_text}</div>
        </div>
        """
    
    table_html += """
        </div>
        
        <div style="
            background: #f8f8f8;
            padding: 12px;
            border-top: 1px solid #e0e0e0;
            text-align: center;
            font-size: 11px;
            color: #666;
        ">
            <strong>📋</strong> = Recipe card included • Simple items shown in overview only
        </div>
    </div>
    """
    
    return table_html

if __name__ == "__main__":
    # Test the filtering system
    from src.models import Dish, Ingredient
    
    # Create test dishes
    test_dishes = [
        Dish(name="Ragi Dosa", meal_type="breakfast", cook_minutes=20, difficulty=2, 
             ingredients=[Ingredient("ragi flour", 120, "g")], steps=["Mix batter", "Cook on tawa"], tags=[], flavor_text=""),
        Dish(name="Banana Slices", meal_type="breakfast", cook_minutes=2, difficulty=1,
             ingredients=[Ingredient("banana", 1, "piece")], steps=["Slice and serve"], tags=[], flavor_text=""),
        Dish(name="Fresh Fruit Bowl", meal_type="snack", cook_minutes=5, difficulty=1,
             ingredients=[Ingredient("fruits", 150, "g")], steps=["Cut and arrange"], tags=[], flavor_text=""),
        Dish(name="Gujarati Dal", meal_type="lunch", cook_minutes=30, difficulty=2,
             ingredients=[Ingredient("dal", 100, "g")], steps=["Pressure cook", "Add tempering"], tags=[], flavor_text="")
    ]
    
    print("🔍 RECIPE CARD FILTERING TEST:")
    for dish in test_dishes:
        needs_card = needs_recipe_card(dish)
        print(f"{'📋' if needs_card else '⭕'} {dish.name} ({dish.cook_minutes}min) - {'CARD NEEDED' if needs_card else 'SIMPLE ITEM'}")
    
    print("\n✅ Smart filtering system ready!")
