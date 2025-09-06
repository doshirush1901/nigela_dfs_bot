"""
Pokémon-style recipe cards for email integration
Creates beautiful HTML cards that can be embedded in emails
"""

def generate_recipe_card_html(dish, card_number=1, profile='parents') -> str:
    """Generate flat black and white recipe card with complete details"""
    
    # Get health and nutrition data
    health_score = getattr(dish, 'health_score', 0.6)
    calories = getattr(dish, 'calories', 200)
    protein_g = getattr(dish, 'protein_g', 8)
    carbs_g = getattr(dish, 'carbs_g', 30)
    fats_g = getattr(dish, 'fats_g', 8)
    
    # Get daily percentage based on profile
    if profile == 'kids':
        daily_percent = getattr(dish, 'kids_daily_percent', 12)
        profile_icon = '👶'
        profile_label = 'Kids'
    else:
        daily_percent = getattr(dish, 'parent_daily_percent', 10) 
        profile_icon = '👨‍👩‍👧‍👦'
        profile_label = 'Parents'
    
    # Health score label (black and white)
    if health_score >= 0.8:
        health_label = 'EXCELLENT'
        health_stars = '★★★★★'
    elif health_score >= 0.6:
        health_label = 'VERY GOOD'
        health_stars = '★★★★☆'
    elif health_score >= 0.4:
        health_label = 'GOOD'
        health_stars = '★★★☆☆'
    else:
        health_label = 'BASIC'
        health_stars = '★★☆☆☆'
    
    # Check for video link - generate if not present
    video_url = getattr(dish, 'video_url', None)
    video_title = getattr(dish, 'video_title', None)
    if not video_url:
        # Create search URL for recipe
        import urllib.parse
        search_query = f"{dish.name} recipe cooking"
        video_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(search_query)}"
        video_title = f"Search: {dish.name} Recipe"
    
    # Create difficulty stars
    difficulty = getattr(dish, 'difficulty', 2)
    stars = '⭐' * difficulty
    
    # Get tags for display
    tags = getattr(dish, 'tags', [])
    display_tags = [tag.replace(':', ' ').title() for tag in tags[:3]]
    
    # Get ingredients for display
    ingredients = getattr(dish, 'ingredients', [])
    ingredient_list = []
    for ing in ingredients[:4]:  # Show first 4 ingredients
        item = getattr(ing, 'item', str(ing))
        qty = getattr(ing, 'qty', 0)
        unit = getattr(ing, 'unit', '')
        if qty > 0:
            ingredient_list.append(f"{item} ({qty}{unit})")
        else:
            ingredient_list.append(item)
    
    if len(ingredients) > 4:
        ingredient_list.append("...")
    
    # Get cooking steps
    steps = getattr(dish, 'steps', ['Follow traditional method'])
    quick_steps = " → ".join(steps[:3])
    if len(steps) > 3:
        quick_steps += "..."
    
    # Get flavor text
    flavor_text = getattr(dish, 'flavor_text', 'A delightful dish for the family.')
    
    # Visual nutrition bars
    protein_bar_width = min(100, (protein_g / 25) * 100)  # Max 25g protein = 100%
    carbs_bar_width = min(100, (carbs_g / 60) * 100)      # Max 60g carbs = 100%
    fat_bar_width = min(100, (fats_g / 20) * 100)         # Max 20g fat = 100%
    health_bar_width = health_score * 100
    
    # Meal type emoji
    meal_emoji = {
        'breakfast': '🌅', 'lunch': '☀️', 'dinner': '🌙', 
        'snack': '🍎', 'morning_snack': '🥝', 'evening_snack': '☕'
    }.get(dish.meal_type, '🍽️')
    
    # Generate flat iPhone-friendly card
    card_html = f"""
    <div style="
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        margin: 12px auto;
        max-width: 350px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    ">
        <!-- Flat Header -->
        <div style="
            background: {health_color};
            color: white;
            padding: 16px;
            text-align: center;
        ">
            <div style="font-size: 24px; margin-bottom: 4px;">{meal_emoji}</div>
            <h3 style="margin: 0; font-size: 18px; font-weight: 600;">{dish.name}</h3>
            <div style="font-size: 13px; margin-top: 6px; opacity: 0.95;">
                🏥 {health_label} • {health_score:.1f}/1.0
            </div>
        </div>
        
        <!-- Quick Stats -->
        <div style="padding: 16px; background: #f8f9fa;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                <span style="font-size: 14px;"><strong>⏱️ {dish.cook_minutes} min</strong></span>
                <span style="font-size: 14px;"><strong>👨‍🍳 {stars}</strong></span>
                <span style="font-size: 14px;"><strong>🔥 {calories} kcal</strong></span>
            </div>
        </div>
        
        <!-- Visual Nutrition Bars -->
        <div style="padding: 16px; background: white;">
            <h4 style="margin: 0 0 12px 0; color: #333; font-size: 15px;">📊 Nutrition Breakdown</h4>
            
            <!-- Protein Bar -->
            <div style="margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                    <span style="font-size: 12px; color: #666;">🥩 Protein</span>
                    <span style="font-size: 12px; font-weight: bold;">{protein_g:.1f}g</span>
                </div>
                <div style="background: #f0f0f0; height: 6px; border-radius: 3px; overflow: hidden;">
                    <div style="background: #ff6b6b; height: 100%; width: {protein_bar_width:.0f}%; border-radius: 3px;"></div>
                </div>
            </div>
            
            <!-- Carbs Bar -->
            <div style="margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                    <span style="font-size: 12px; color: #666;">🍞 Carbs</span>
                    <span style="font-size: 12px; font-weight: bold;">{carbs_g:.1f}g</span>
                </div>
                <div style="background: #f0f0f0; height: 6px; border-radius: 3px; overflow: hidden;">
                    <div style="background: #4ecdc4; height: 100%; width: {carbs_bar_width:.0f}%; border-radius: 3px;"></div>
                </div>
            </div>
            
            <!-- Fats Bar -->
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                    <span style="font-size: 12px; color: #666;">🥑 Fats</span>
                    <span style="font-size: 12px; font-weight: bold;">{fats_g:.1f}g</span>
                </div>
                <div style="background: #f0f0f0; height: 6px; border-radius: 3px; overflow: hidden;">
                    <div style="background: #45b7d1; height: 100%; width: {fat_bar_width:.0f}%; border-radius: 3px;"></div>
                </div>
            </div>
            
            <!-- Daily Contribution -->
            <div style="
                background: {'#e8f5e8' if profile == 'kids' else '#fff3e0'};
                padding: 12px;
                border-radius: 8px;
                text-align: center;
                border: 2px solid {'#4CAF50' if profile == 'kids' else '#FF9800'};
            ">
                <div style="font-size: 13px; font-weight: bold; color: #333;">
                    {profile_icon} {profile_focus}
                </div>
                <div style="font-size: 16px; font-weight: bold; color: {'#2e7d32' if profile == 'kids' else '#f57c00'}; margin-top: 4px;">
                    {daily_percent:.1f}% of daily calories
                </div>
            </div>
        </div>
        
        <!-- Ingredients Section -->
        <div style="padding: 16px; background: white; border-bottom: 1px solid #e0e0e0;">
            <h4 style="margin: 0 0 8px 0; color: #000; font-size: 14px; font-weight: 700;">🥘 INGREDIENTS</h4>
            <ul style="margin: 0; padding-left: 16px; font-size: 13px; line-height: 1.6; color: #333;">
                {''.join([f'<li style="margin-bottom: 3px;">{ingredient}</li>' for ingredient in ingredient_list])}
            </ul>
        </div>
        
        <!-- Method Section -->
        <div style="padding: 16px; background: white; border-bottom: 1px solid #e0e0e0;">
            <h4 style="margin: 0 0 8px 0; color: #000; font-size: 14px; font-weight: 700;">👩‍🍳 METHOD</h4>
            <ol style="margin: 0; padding-left: 16px; font-size: 13px; line-height: 1.6; color: #333;">
                {''.join([f'<li style="margin-bottom: 4px;">{step}</li>' for step in dish.steps])}
            </ol>
        </div>
        
        <!-- Nigela's Note -->
        <div style="
            background: #f8f8f8;
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
            font-style: italic;
        ">
            <div style="font-size: 12px; color: #666;">
                💬 <strong>Nigela:</strong> "{flavor_text}"
            </div>
        </div>
        
        <!-- YouTube Video Link -->
        <div style="
            background: #000000;
            padding: 12px;
            text-align: center;
        ">
            <a href="{video_url}" target="_blank" style="
                color: white;
                text-decoration: none;
                font-size: 13px;
                font-weight: 700;
                display: block;
                letter-spacing: 0.5px;
            ">
                ▶ WATCH RECIPE VIDEO
            </a>
            <div style="font-size: 10px; color: #ccc; margin-top: 4px;">
                {video_title[:40] if video_title else 'Recipe tutorial'}
            </div>
        </div>
        
        <!-- Card Number -->
        <div style="
            background: #f8f8f8;
            padding: 8px;
            text-align: center;
            font-size: 10px;
            color: #999;
            font-weight: 600;
        ">
            CARD #{card_number:03d}
        </div>
    </div>
    """
    
    return card_html

def generate_meal_section_html(meal_name: str, dishes: dict, start_card_num: int = 1) -> str:
    """Generate HTML for a complete meal section with multiple cards"""
    
    meal_icons = {
        'breakfast': '🌅',
        'morning_snack': '🍎', 
        'lunch': '🍽️',
        'evening_snack': '🍿',
        'dinner': '🌙'
    }
    
    meal_icon = meal_icons.get(meal_name, '🍴')
    
    section_html = f"""
    <div style="margin: 25px 0;">
        <h2 style="
            color: #d4691a;
            text-align: center;
            font-size: 24px;
            margin-bottom: 20px;
            padding: 10px;
            background: linear-gradient(45deg, #fff5ee, #fef7f0);
            border-radius: 10px;
        ">
            {meal_icon} {meal_name.replace('_', ' ').title()}
        </h2>
        
        <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px;">
    """
    
    card_num = start_card_num
    for slot_name, dish in dishes.items():
        card_html = generate_recipe_card_html(dish, card_num)
        section_html += card_html
        card_num += 1
    
    section_html += """
        </div>
    </div>
    """
    
    return section_html, card_num

def generate_meal_overview_table(plan: dict) -> str:
    """Generate overview table with smart card indicators"""
    
    from .recipe_filter import needs_recipe_card
    
    # Collect all dishes organized by meal
    meals_data = {
        'Breakfast': [],
        'Morning Snack': [],
        'Lunch': [],
        'Evening Snack': [],
        'Dinner': []
    }
    
    meal_mapping = {
        'breakfast': 'Breakfast',
        'morning_snack': 'Morning Snack', 
        'lunch': 'Lunch',
        'evening_snack': 'Evening Snack',
        'dinner': 'Dinner'
    }
    
    for meal_key, dishes in plan.items():
        meal_name = meal_mapping.get(meal_key, meal_key.title())
        for slot, dish in dishes.items():
            # Add indicator for recipe cards
            if needs_recipe_card(dish):
                meals_data[meal_name].append(f"<strong>{dish.name}</strong> 📋")
            else:
                meals_data[meal_name].append(dish.name)
    
    # Generate table HTML
    table_html = """
    <div style="
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 24px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    ">
        <h2 style="
            margin: 0 0 16px 0;
            color: #1d1d1f;
            font-size: 20px;
            text-align: center;
            font-weight: 700;
        ">📋 Today's Menu at a Glance</h2>
        
        <div style="overflow-x: auto;">
            <table style="
                width: 100%;
                border-collapse: collapse;
                font-size: 13px;
                background: #f8f9fa;
                border-radius: 12px;
                overflow: hidden;
            ">
                <thead>
                    <tr style="background: #e3f2fd;">
                        <th style="padding: 12px 8px; text-align: left; font-weight: 600; color: #1d1d1f; border-bottom: 2px solid #bbdefb;">Meal</th>
                        <th style="padding: 12px 8px; text-align: left; font-weight: 600; color: #1d1d1f; border-bottom: 2px solid #bbdefb;">Items</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    meal_emojis = {
        'Breakfast': '🌅',
        'Morning Snack': '🥝',
        'Lunch': '☀️', 
        'Evening Snack': '☕',
        'Dinner': '🌙'
    }
    
    for meal_name, dishes in meals_data.items():
        if dishes:  # Only show meals with dishes
            emoji = meal_emojis.get(meal_name, '🍽️')
            dishes_text = ' • '.join(dishes) if dishes else 'No items planned'
            
            table_html += f"""
                    <tr style="border-bottom: 1px solid #e0e0e0;">
                        <td style="padding: 12px 8px; font-weight: 600; color: #333; vertical-align: top;">
                            {emoji} {meal_name}
                        </td>
                        <td style="padding: 12px 8px; color: #666; line-height: 1.4;">
                            {dishes_text}
                        </td>
                    </tr>
            """
    
    table_html += """
                </tbody>
            </table>
        </div>
    </div>
    """
    
    return table_html

def generate_nutrition_summary(plan: dict) -> str:
    """Generate daily nutrition summary"""
    
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fats = 0
    meal_count = 0
    
    # Calculate totals
    for meal_dishes in plan.values():
        for dish in meal_dishes.values():
            total_calories += getattr(dish, 'calories', 200)
            total_protein += getattr(dish, 'protein_g', 8)
            total_carbs += getattr(dish, 'carbs_g', 30)
            total_fats += getattr(dish, 'fats_g', 8)
            meal_count += 1
    
    # Calculate percentages for both profiles
    parent_percent = (total_calories / 1800) * 100
    kids_percent = (total_calories / 1600) * 100
    
    summary_html = f"""
    <div style="
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin: 24px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    ">
        <h2 style="
            margin: 0 0 16px 0;
            color: #1d1d1f;
            font-size: 20px;
            text-align: center;
            font-weight: 700;
        ">📊 Daily Nutrition Summary</h2>
        
        <div style="display: flex; gap: 12px; margin-bottom: 20px;">
            <!-- Parents Profile -->
            <div style="
                flex: 1;
                background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
                padding: 16px;
                border-radius: 12px;
                text-align: center;
                border: 2px solid #FF9800;
            ">
                <div style="font-size: 24px; margin-bottom: 8px;">👨‍👩‍👧‍👦</div>
                <div style="font-size: 16px; font-weight: bold; color: #1d1d1f;">Parents</div>
                <div style="font-size: 12px; color: #666; margin: 4px 0;">Calorie Deficit Plan</div>
                <div style="font-size: 24px; font-weight: bold; color: #f57c00; margin: 8px 0;">{parent_percent:.0f}%</div>
                <div style="font-size: 11px; color: #999;">of 1800 daily calories</div>
                <div style="font-size: 13px; color: #666; margin-top: 8px;">
                    🔥 {total_calories} kcal<br>
                    🥩 {total_protein:.0f}g protein
                </div>
            </div>
            
            <!-- Kids Profile -->
            <div style="
                flex: 1;
                background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c8 100%);
                padding: 16px;
                border-radius: 12px;
                text-align: center;
                border: 2px solid #4CAF50;
            ">
                <div style="font-size: 24px; margin-bottom: 8px;">👶</div>
                <div style="font-size: 16px; font-weight: bold; color: #1d1d1f;">Kids</div>
                <div style="font-size: 12px; color: #666; margin: 4px 0;">Growth & Immunity</div>
                <div style="font-size: 24px; font-weight: bold; color: #2e7d32; margin: 8px 0;">{kids_percent:.0f}%</div>
                <div style="font-size: 11px; color: #999;">of 1600 daily calories</div>
                <div style="font-size: 13px; color: #666; margin-top: 8px;">
                    🔥 {total_calories} kcal<br>
                    💪 Immune support
                </div>
            </div>
        </div>
        
        <!-- Macro Breakdown -->
        <div style="background: #f8f9fa; padding: 16px; border-radius: 12px;">
            <h4 style="margin: 0 0 12px 0; color: #1d1d1f; font-size: 16px; text-align: center;">🥄 Total Daily Macros</h4>
            <div style="display: flex; justify-content: space-around; text-align: center;">
                <div>
                    <div style="font-size: 18px; color: #ff6b6b; font-weight: bold;">{total_protein:.0f}g</div>
                    <div style="font-size: 12px; color: #666;">🥩 Protein</div>
                </div>
                <div>
                    <div style="font-size: 18px; color: #4ecdc4; font-weight: bold;">{total_carbs:.0f}g</div>
                    <div style="font-size: 12px; color: #666;">🍞 Carbs</div>
                </div>
                <div>
                    <div style="font-size: 18px; color: #45b7d1; font-weight: bold;">{total_fats:.0f}g</div>
                    <div style="font-size: 12px; color: #666;">🥑 Fats</div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return summary_html

def generate_daily_tips() -> str:
    """Generate daily cooking tips and wisdom"""
    
    tips_html = '''
    <div style="
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin: 24px 0;
        border-left: 4px solid #ff6b6b;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    ">
        <h2 style="
            margin: 0 0 16px 0;
            color: #1d1d1f;
            font-size: 20px;
            font-weight: 700;
        ">💡 Nigela's Daily Wisdom</h2>
        
        <div style="font-size: 15px; color: #333; line-height: 1.6; margin-bottom: 16px;">
            <strong>"Today's cooking mantra: Prep with purpose, cook with love, serve with joy."</strong>
        </div>
        
        <div style="background: #f8f9fa; padding: 16px; border-radius: 12px;">
            <h4 style="margin: 0 0 12px 0; color: #1d1d1f; font-size: 16px;">🕐 Smart Cooking Tips</h4>
            <ul style="margin: 0; padding-left: 20px; color: #666; font-size: 14px;">
                <li style="margin-bottom: 8px;"><strong>Morning prep:</strong> Soak dal for lunch while making breakfast</li>
                <li style="margin-bottom: 8px;"><strong>Batch cooking:</strong> Make extra dal - it tastes better the next day</li>
                <li style="margin-bottom: 8px;"><strong>Spice blooming:</strong> Heat whole spices in oil first for deeper flavor</li>
                <li style="margin-bottom: 8px;"><strong>Kids tip:</strong> Let them help with simple tasks - builds food connection</li>
                <li style="margin-bottom: 8px;"><strong>Health hack:</strong> Add a pinch of turmeric to everything - natural immunity</li>
            </ul>
        </div>
    </div>
    '''
    
    return tips_html

def generate_grocery_section(plan: dict) -> str:
    """Generate grocery check and Blinkit ordering section"""
    
    # Collect all ingredients from the day's meals
    all_ingredients = []
    for meal_dishes in plan.values():
        for dish in meal_dishes.values():
            for ingredient in getattr(dish, 'ingredients', []):
                item = getattr(ingredient, 'item', str(ingredient))
                if item and item not in all_ingredients:
                    all_ingredients.append(item)
    
    # Common pantry staples to check
    pantry_staples = [
        'rice', 'dal', 'oil', 'ghee', 'salt', 'turmeric', 'cumin seeds',
        'mustard seeds', 'ginger', 'green chilies', 'coriander leaves'
    ]
    
    grocery_html = f'''
    <div style="
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin: 24px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    ">
        <h2 style="
            margin: 0 0 16px 0;
            color: #1d1d1f;
            font-size: 20px;
            font-weight: 700;
            text-align: center;
        ">🛒 Grocery Check & Shopping</h2>
        
        <!-- Fridge Check Section -->
        <div style="background: #e8f5e8; padding: 16px; border-radius: 12px; margin-bottom: 16px;">
            <h4 style="margin: 0 0 12px 0; color: #2e7d32; font-size: 16px;">🧊 Check Your Fridge</h4>
            <p style="margin: 0 0 12px 0; color: #666; font-size: 14px;">Make sure you have these essentials:</p>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                {' '.join([f'<span style="background: white; padding: 6px 12px; border-radius: 20px; font-size: 12px; color: #2e7d32; border: 1px solid #4CAF50;">✓ {item}</span>' for item in pantry_staples[:8]])}
            </div>
        </div>
        
        <!-- Today's Special Ingredients -->
        <div style="background: #fff3e0; padding: 16px; border-radius: 12px; margin-bottom: 16px;">
            <h4 style="margin: 0 0 12px 0; color: #f57c00; font-size: 16px;">🥘 Today's Special Ingredients</h4>
            <ul style="margin: 0; padding-left: 20px; color: #666; font-size: 14px;">
                {' '.join([f'<li style="margin-bottom: 4px;">{ingredient}</li>' for ingredient in all_ingredients[:8]])}
                {f'<li style="color: #999; font-style: italic;">...and {len(all_ingredients) - 8} more</li>' if len(all_ingredients) > 8 else ''}
            </ul>
        </div>
        
        <!-- Blinkit Quick Order -->
        <div style="
            background: linear-gradient(135deg, #ff4757 0%, #ff3838 100%);
            padding: 16px;
            border-radius: 12px;
            text-align: center;
            color: white;
        ">
            <h4 style="margin: 0 0 8px 0; font-size: 16px; font-weight: 700;">🚀 Quick Grocery Delivery</h4>
            <p style="margin: 0 0 12px 0; font-size: 14px; opacity: 0.9;">Missing ingredients? Get them delivered in 10 minutes!</p>
            
            <div style="display: flex; gap: 8px; justify-content: center;">
                <div style="
                    background: rgba(255,255,255,0.2);
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-size: 13px;
                    font-weight: 600;
                ">
                    📱 Blinkit App
                </div>
                <div style="
                    background: rgba(255,255,255,0.2);
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-size: 13px;
                    font-weight: 600;
                ">
                    🛒 BigBasket
                </div>
                <div style="
                    background: rgba(255,255,255,0.2);
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-size: 13px;
                    font-weight: 600;
                ">
                    🥬 Grofers
                </div>
            </div>
        </div>
    </div>
    '''
    
    return grocery_html

def generate_complete_menu_email_html(plan: dict, date_str: str) -> str:
    """Generate complete iPhone-optimized email: table → cards → nutrition → tips → groceries"""
    
    email_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nigela Daily Menu</title>
    </head>
    <body style="
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: #f2f2f7;
        margin: 0;
        padding: 16px;
        line-height: 1.4;
    ">
        <div style="max-width: 350px; margin: 0 auto;">
            
            <!-- Header -->
            <div style="
                background: white;
                padding: 24px;
                border-radius: 16px;
                text-align: center;
                margin-bottom: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            ">
                <div style="font-size: 32px; margin-bottom: 8px;">🍽️</div>
                <h1 style="margin: 0; font-size: 24px; color: #1d1d1f; font-weight: 700;">Nigela's Daily Menu</h1>
                <p style="margin: 8px 0 0 0; color: #86868b; font-size: 16px;">{date_str}</p>
                <p style="margin: 4px 0 0 0; color: #86868b; font-size: 14px;">Complete Health-Focused Meal Plan</p>
            </div>
            
            <!-- Quick Overview Table -->
            {generate_meal_overview_table(plan)}
            
            <!-- Introduction -->
            <div style="
                background: white;
                padding: 20px;
                border-radius: 16px;
                margin-bottom: 20px;
                border-left: 4px solid #ff6b6b;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            ">
                <div style="font-size: 18px; margin-bottom: 8px; text-align: center;">💕</div>
                <p style="color: #333; line-height: 1.5; margin: 0; font-size: 15px; text-align: center; font-style: italic;">
                    "Today's meals are crafted with your health and happiness in mind. Each recipe includes nutrition data to help you make informed choices for your family."
                </p>
                <p style="color: #ff6b6b; text-align: center; margin: 12px 0 0 0; font-weight: 600; font-size: 14px;">
                    - With love, Nigela ✨
                </p>
            </div>
    """
    
    # Add detailed recipe cards for each meal
    card_counter = 1
    meal_order = ['breakfast', 'morning_snack', 'lunch', 'evening_snack', 'dinner']
    
    for meal in meal_order:
        if meal in plan and plan[meal]:
            section_html, card_counter = generate_meal_section_html(meal, plan[meal], card_counter)
            email_html += section_html
    
    # Add nutrition summary
    email_html += generate_nutrition_summary(plan)
    
    # Add daily tips
    email_html += generate_daily_tips()
    
    # Add grocery section
    email_html += generate_grocery_section(plan)
    
    # Footer
    email_html += f"""
            <!-- Footer -->
            <div style="
                background: white;
                padding: 20px;
                border-radius: 16px;
                margin-top: 20px;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            ">
                <div style="font-size: 18px; margin-bottom: 8px;">🙏</div>
                <p style="color: #666; font-size: 14px; line-height: 1.5; margin: 0;">
                    Thank you for letting Nigela be part of your family's daily nourishment journey.
                </p>
                <p style="color: #86868b; font-size: 12px; margin: 12px 0 0 0;">
                    Generated by Nigela AI Cooking Assistant<br>
                    Powered by OpenAI • Made with 💚 for your family
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return email_html
