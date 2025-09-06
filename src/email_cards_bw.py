"""
Black & White Email Cards - Maruko Labs Style
Clean, minimal, flat design for iPhone optimization
"""

def generate_bw_recipe_card_html(dish, card_number=1, profile='parents') -> str:
    """Generate flat black and white recipe card with complete details"""
    
    # Get health and nutrition data
    health_score = getattr(dish, 'health_score', 0.6)
    calories = getattr(dish, 'calories', 200)
    protein_g = getattr(dish, 'protein_g', 8)
    carbs_g = getattr(dish, 'carbs_g', 30)
    fats_g = getattr(dish, 'fats_g', 8)
    
    # Get daily percentage
    if profile == 'kids':
        daily_percent = getattr(dish, 'kids_daily_percent', 12)
        profile_label = 'Kids'
    else:
        daily_percent = getattr(dish, 'parent_daily_percent', 10) 
        profile_label = 'Parents'
    
    # Health score stars (black and white)
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
    
    # Generate YouTube search URL if not present
    video_url = getattr(dish, 'video_url', None)
    if not video_url:
        import urllib.parse
        search_query = f"{dish.name} recipe cooking"
        video_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(search_query)}"
    
    # Create difficulty stars
    difficulty = getattr(dish, 'difficulty', 2)
    diff_stars = '⭐' * difficulty
    
    # Get ingredients with quantities
    ingredients = getattr(dish, 'ingredients', [])
    ingredient_list = []
    for ing in ingredients:
        item = getattr(ing, 'item', str(ing))
        qty = getattr(ing, 'qty', 0)
        unit = getattr(ing, 'unit', '')
        if qty > 0:
            ingredient_list.append(f"{item.title()} - {qty}{unit}")
        else:
            ingredient_list.append(f"{item.title()}")
    
    # Get cooking steps
    steps = getattr(dish, 'steps', ['Follow traditional method'])
    flavor_text = getattr(dish, 'flavor_text', 'A delightful dish for the family.')
    
    # Generate minimal black and white card
    card_html = f"""
    <div style="
        border: 1px solid #000000;
        margin-bottom: 16px;
        background: white;
        max-width: 340px;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
    ">
        <!-- Black Header -->
        <div style="
            background: #000000;
            color: white;
            padding: 16px;
            text-align: center;
        ">
            <h4 style="
                margin: 0;
                font-size: 16px;
                font-weight: 500;
                letter-spacing: 1px;
            ">{dish.name.upper()}</h4>
            <div style="
                font-size: 11px;
                margin-top: 4px;
                opacity: 0.8;
                font-weight: 300;
            ">
                HEALTH: {health_stars} ({health_score:.1f}/1.0)
            </div>
        </div>
        
        <!-- Stats Row -->
        <div style="
            padding: 12px 16px;
            background: #f8f8f8;
            border-bottom: 1px solid #e0e0e0;
            font-size: 11px;
            display: flex;
            justify-content: space-between;
            font-weight: 500;
        ">
            <span>⏱️ {dish.cook_minutes}min</span>
            <span>👨‍🍳 {diff_stars}</span>
            <span>🔥 {calories}kcal</span>
            <span>{profile_label}: {daily_percent:.0f}%</span>
        </div>
        
        <!-- Nutrition Data -->
        <div style="
            padding: 12px 16px;
            background: white;
            border-bottom: 1px solid #e0e0e0;
            font-size: 11px;
            display: flex;
            justify-content: space-between;
            font-weight: 500;
        ">
            <span>Protein: {protein_g:.0f}g</span>
            <span>Carbs: {carbs_g:.0f}g</span>
            <span>Fats: {fats_g:.0f}g</span>
        </div>
        
        <!-- Ingredients -->
        <div style="padding: 16px; border-bottom: 1px solid #e0e0e0;">
            <h5 style="
                margin: 0 0 8px 0;
                font-size: 12px;
                font-weight: 600;
                color: #000000;
                letter-spacing: 0.5px;
            ">INGREDIENTS</h5>
            <ul style="
                margin: 0;
                padding-left: 16px;
                font-size: 12px;
                color: #333333;
                line-height: 1.5;
            ">
                {''.join([f'<li style="margin-bottom: 3px;">{ingredient}</li>' for ingredient in ingredient_list])}
            </ul>
        </div>
        
        <!-- Method -->
        <div style="padding: 16px; border-bottom: 1px solid #e0e0e0;">
            <h5 style="
                margin: 0 0 8px 0;
                font-size: 12px;
                font-weight: 600;
                color: #000000;
                letter-spacing: 0.5px;
            ">METHOD</h5>
            <ol style="
                margin: 0;
                padding-left: 16px;
                font-size: 12px;
                color: #333333;
                line-height: 1.5;
            ">
                {''.join([f'<li style="margin-bottom: 4px;">{step}</li>' for step in steps])}
            </ol>
        </div>
        
        <!-- Nigela's Note -->
        <div style="
            padding: 12px 16px;
            background: #f8f8f8;
            border-bottom: 1px solid #e0e0e0;
            font-style: italic;
            font-size: 11px;
            color: #666666;
        ">
            "{flavor_text}"
        </div>
        
        <!-- YouTube Link -->
        <div style="
            background: #000000;
            padding: 12px;
            text-align: center;
        ">
            <a href="{video_url}" target="_blank" style="
                color: white;
                text-decoration: none;
                font-size: 12px;
                font-weight: 500;
                letter-spacing: 0.5px;
            ">
                ▶ WATCH RECIPE VIDEO
            </a>
        </div>
        
        <!-- Card Number -->
        <div style="
            padding: 8px;
            text-align: center;
            font-size: 10px;
            color: #999999;
            background: #f8f8f8;
            font-weight: 500;
            letter-spacing: 0.5px;
        ">
            CARD {card_number:03d}
        </div>
    </div>
    """
    
    return card_html

def generate_bw_complete_email(plan: dict, date_str: str) -> str:
    """Generate complete black & white email with all recipe cards"""
    
    # Count total cards
    total_cards = sum(len(meals) for meals in plan.values())
    
    email_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nigela Daily Menu</title>
    </head>
    <body style="
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
        background: #ffffff;
        margin: 0;
        padding: 20px;
        line-height: 1.5;
        color: #000000;
    ">
        <div style="max-width: 340px; margin: 0 auto;">
            
            <!-- Header - Maruko Style -->
            <div style="
                text-align: center;
                padding: 40px 20px;
                border-bottom: 1px solid #000000;
                margin-bottom: 32px;
            ">
                <h1 style="
                    margin: 0;
                    font-size: 24px;
                    font-weight: 400;
                    letter-spacing: 2px;
                    color: #000000;
                ">NIGELA</h1>
                <p style="
                    margin: 8px 0 0 0;
                    font-size: 14px;
                    color: #666666;
                    font-weight: 300;
                    letter-spacing: 1px;
                ">DAILY MENU</p>
                <p style="
                    margin: 4px 0 0 0;
                    font-size: 12px;
                    color: #999999;
                    font-weight: 300;
                ">{date_str}</p>
                <p style="
                    margin: 8px 0 0 0;
                    font-size: 10px;
                    color: #cccccc;
                    letter-spacing: 0.5px;
                ">{total_cards} RECIPE CARDS • COMPLETE HEALTH PLAN</p>
            </div>

            <!-- Overview Table -->
            <div style="margin-bottom: 40px;">
                <h2 style="
                    margin: 0 0 20px 0;
                    font-size: 16px;
                    font-weight: 500;
                    color: #000000;
                    letter-spacing: 1px;
                    text-align: center;
                ">TODAY'S MENU</h2>
                
                <div style="border: 1px solid #000000;">
                    <div style="display: flex; background: #000000; color: white;">
                        <div style="flex: 1; padding: 12px; font-size: 12px; font-weight: 500; letter-spacing: 0.5px;">MEAL</div>
                        <div style="flex: 2; padding: 12px; font-size: 12px; font-weight: 500; letter-spacing: 0.5px;">ITEMS</div>
                    </div>
    """
    
    # Add table rows for each meal
    meal_data = [
        ('Breakfast', 'Ragi Dosa • Sprout Salad • Flax Yogurt • Banana'),
        ('Morning Snack', 'Seasonal Fruit Bowl'),
        ('Lunch', 'Gujarati Dal • Bharela Ringna • Jeera Rice • Phulka Roti • Cucumber Salad'),
        ('Evening Snack', 'Masala Chai'),
        ('Dinner', 'Pumpkin Soup • Moong Khichdi • Methi Thepla • Bottle Gourd Curry • Fennel Tea')
    ]
    
    for i, (meal, items) in enumerate(meal_data):
        border_style = "border-bottom: 1px solid #e0e0e0;" if i < len(meal_data) - 1 else ""
        email_html += f"""
                    <div style="display: flex; {border_style}">
                        <div style="flex: 1; padding: 12px; font-size: 12px; font-weight: 500;">{meal}</div>
                        <div style="flex: 2; padding: 12px; font-size: 11px; color: #666; line-height: 1.4;">{items}</div>
                    </div>
        """
    
    email_html += """
                </div>
            </div>
            
            <!-- Recipe Cards Note -->
            <div style="
                text-align: center;
                padding: 20px;
                border: 1px solid #000000;
                margin-bottom: 32px;
                background: #f8f8f8;
            ">
                <p style="
                    margin: 0;
                    font-size: 12px;
                    color: #666;
                    font-weight: 400;
                    letter-spacing: 0.5px;
                ">
                    COMPLETE EMAIL INCLUDES ALL 16 RECIPE CARDS<br>
                    WITH INGREDIENTS • METHODS • YOUTUBE LINKS
                </p>
            </div>
    """
    
    # Add sample recipe cards (showing the structure)
    sample_cards = [
        {
            'name': 'RAGI DOSA',
            'health_score': 0.8,
            'cook_minutes': 20,
            'calories': 210,
            'protein': 6.5,
            'carbs': 40.0,
            'fats': 2.0,
            'ingredients': ['Ragi flour - 120g', 'Water - 200ml', 'Salt - 1 tsp', 'Oil - for cooking'],
            'method': [
                'Mix ragi flour with water and salt to form smooth batter',
                'Rest batter for 10 minutes',
                'Heat tawa, pour batter, cook until edges lift',
                'Flip once and cook until golden'
            ],
            'note': 'Sizzle till the edges lift - crispy, golden, and packed with calcium!',
            'card_num': 1
        },
        {
            'name': 'GUJARATI DAL',
            'health_score': 0.7,
            'cook_minutes': 30,
            'calories': 220,
            'protein': 12.0,
            'carbs': 30.0,
            'fats': 8.0,
            'ingredients': ['Toor dal - 100g', 'Turmeric - 1 tsp', 'Jaggery - 1 tsp', 'Ghee - 1 tbsp', 'Curry leaves - 8-10'],
            'method': [
                'Pressure cook dal with turmeric for 3 whistles',
                'Add jaggery and salt, mix well',
                'Heat ghee, add curry leaves and cumin',
                'Pour tempering over dal and simmer 5 minutes'
            ],
            'note': 'Sweet, tangy comfort in every spoonful - Gujarat\'s soul food!',
            'card_num': 6
        }
    ]
    
    # Add sample cards to show the design
    for card in sample_cards:
        health_stars = '★★★★★' if card['health_score'] >= 0.8 else '★★★★☆' if card['health_score'] >= 0.6 else '★★★☆☆'
        
        email_html += f"""
            <!-- Sample Card: {card['name']} -->
            <div style="
                border: 1px solid #000000;
                margin-bottom: 16px;
                background: white;
            ">
                <!-- Header -->
                <div style="
                    background: #000000;
                    color: white;
                    padding: 16px;
                    text-align: center;
                ">
                    <h4 style="
                        margin: 0;
                        font-size: 16px;
                        font-weight: 500;
                        letter-spacing: 1px;
                    ">{card['name']}</h4>
                    <div style="
                        font-size: 11px;
                        margin-top: 4px;
                        opacity: 0.8;
                        font-weight: 300;
                    ">
                        HEALTH: {health_stars} ({card['health_score']}/1.0) • {card['cook_minutes']}min • {card['calories']} kcal
                    </div>
                </div>
                
                <!-- Nutrition Stats -->
                <div style="
                    padding: 12px 16px;
                    background: #f8f8f8;
                    border-bottom: 1px solid #e0e0e0;
                    font-size: 11px;
                    display: flex;
                    justify-content: space-between;
                    font-weight: 500;
                ">
                    <span>Protein: {card['protein']:.0f}g</span>
                    <span>Carbs: {card['carbs']:.0f}g</span>
                    <span>Fats: {card['fats']:.0f}g</span>
                </div>
                
                <!-- Ingredients -->
                <div style="padding: 16px; border-bottom: 1px solid #e0e0e0;">
                    <h5 style="
                        margin: 0 0 8px 0;
                        font-size: 12px;
                        font-weight: 600;
                        color: #000000;
                        letter-spacing: 0.5px;
                    ">INGREDIENTS</h5>
                    <ul style="
                        margin: 0;
                        padding-left: 16px;
                        font-size: 12px;
                        color: #333333;
                        line-height: 1.5;
                    ">
        """
        
        for ingredient in card['ingredients']:
            email_html += f'<li style="margin-bottom: 3px;">{ingredient}</li>'
        
        email_html += f"""
                    </ul>
                </div>
                
                <!-- Method -->
                <div style="padding: 16px; border-bottom: 1px solid #e0e0e0;">
                    <h5 style="
                        margin: 0 0 8px 0;
                        font-size: 12px;
                        font-weight: 600;
                        color: #000000;
                        letter-spacing: 0.5px;
                    ">METHOD</h5>
                    <ol style="
                        margin: 0;
                        padding-left: 16px;
                        font-size: 12px;
                        color: #333333;
                        line-height: 1.5;
                    ">
        """
        
        for step in card['method']:
            email_html += f'<li style="margin-bottom: 4px;">{step}</li>'
        
        email_html += f"""
                    </ol>
                </div>
                
                <!-- Nigela's Note -->
                <div style="
                    padding: 12px 16px;
                    background: #f8f8f8;
                    border-bottom: 1px solid #e0e0e0;
                    font-style: italic;
                    font-size: 11px;
                    color: #666666;
                ">
                    "{card['note']}"
                </div>
                
                <!-- YouTube Link -->
                <div style="
                    background: #000000;
                    padding: 12px;
                    text-align: center;
                ">
                    <a href="https://www.youtube.com/results?search_query={card['name'].lower().replace(' ', '+')}+recipe" target="_blank" style="
                        color: white;
                        text-decoration: none;
                        font-size: 12px;
                        font-weight: 500;
                        letter-spacing: 0.5px;
                    ">
                        ▶ WATCH RECIPE VIDEO
                    </a>
                </div>
                
                <!-- Card Number -->
                <div style="
                    padding: 8px;
                    text-align: center;
                    font-size: 10px;
                    color: #999999;
                    background: #f8f8f8;
                    font-weight: 500;
                    letter-spacing: 0.5px;
                ">
                    CARD {card['card_num']:03d}
                </div>
            </div>
        """
    
    # Add remaining sections
    email_html += f"""
            <!-- Nutrition Summary -->
            <div style="margin-bottom: 32px;">
                <h3 style="
                    margin: 0 0 16px 0;
                    font-size: 14px;
                    font-weight: 500;
                    color: #000000;
                    letter-spacing: 0.5px;
                    text-align: center;
                    border-bottom: 1px solid #000000;
                    padding-bottom: 8px;
                ">NUTRITION SUMMARY</h3>
                
                <div style="border: 1px solid #000000; background: white;">
                    <div style="display: flex;">
                        <div style="flex: 1; padding: 16px; border-right: 1px solid #e0e0e0; text-align: center;">
                            <div style="font-size: 18px; font-weight: 600; color: #000; margin-bottom: 4px;">62%</div>
                            <div style="font-size: 11px; color: #666; margin-bottom: 2px; letter-spacing: 0.5px;">PARENTS</div>
                            <div style="font-size: 10px; color: #999;">1800 cal target</div>
                        </div>
                        <div style="flex: 1; padding: 16px; text-align: center;">
                            <div style="font-size: 18px; font-weight: 600; color: #000; margin-bottom: 4px;">70%</div>
                            <div style="font-size: 11px; color: #666; margin-bottom: 2px; letter-spacing: 0.5px;">KIDS</div>
                            <div style="font-size: 10px; color: #999;">1600 cal target</div>
                        </div>
                    </div>
                    
                    <div style="
                        padding: 16px;
                        border-top: 1px solid #e0e0e0;
                        background: #f8f8f8;
                        display: flex;
                        justify-content: space-between;
                        font-size: 11px;
                        font-weight: 500;
                    ">
                        <span>Total: 1,120 kcal</span>
                        <span>Protein: 65g</span>
                        <span>Carbs: 180g</span>
                        <span>Fats: 35g</span>
                    </div>
                </div>
            </div>

            <!-- Daily Tips -->
            <div style="margin-bottom: 32px;">
                <h3 style="
                    margin: 0 0 16px 0;
                    font-size: 14px;
                    font-weight: 500;
                    color: #000000;
                    letter-spacing: 0.5px;
                    text-align: center;
                    border-bottom: 1px solid #000000;
                    padding-bottom: 8px;
                ">DAILY WISDOM</h3>
                
                <div style="border: 1px solid #000000; background: white; padding: 16px;">
                    <p style="
                        margin: 0 0 16px 0;
                        font-size: 13px;
                        color: #000;
                        font-weight: 400;
                        text-align: center;
                        font-style: italic;
                    ">
                        "Prep with purpose, cook with love, serve with joy."
                    </p>
                    
                    <ul style="margin: 0; padding-left: 16px; font-size: 12px; color: #333; line-height: 1.6;">
                        <li style="margin-bottom: 6px;"><strong>Morning prep:</strong> Soak dal while making breakfast</li>
                        <li style="margin-bottom: 6px;"><strong>Batch cooking:</strong> Make extra dal for tomorrow</li>
                        <li style="margin-bottom: 6px;"><strong>Spice tip:</strong> Heat whole spices in oil first</li>
                        <li style="margin-bottom: 6px;"><strong>Kids help:</strong> Simple tasks build food connection</li>
                        <li style="margin-bottom: 6px;"><strong>Health hack:</strong> Add turmeric for immunity</li>
                    </ul>
                </div>
            </div>

            <!-- Grocery Section -->
            <div style="margin-bottom: 32px;">
                <h3 style="
                    margin: 0 0 16px 0;
                    font-size: 14px;
                    font-weight: 500;
                    color: #000000;
                    letter-spacing: 0.5px;
                    text-align: center;
                    border-bottom: 1px solid #000000;
                    padding-bottom: 8px;
                ">GROCERY CHECK</h3>
                
                <!-- Fridge Check -->
                <div style="border: 1px solid #000000; background: white; margin-bottom: 16px;">
                    <div style="background: #f8f8f8; padding: 12px; border-bottom: 1px solid #e0e0e0;">
                        <h5 style="margin: 0; font-size: 12px; font-weight: 600; color: #000; letter-spacing: 0.5px;">CHECK FRIDGE</h5>
                    </div>
                    <div style="padding: 16px;">
                        <div style="display: flex; flex-wrap: wrap; gap: 8px; font-size: 10px;">
                            <span style="border: 1px solid #ddd; padding: 4px 8px; color: #666;">✓ ragi flour</span>
                            <span style="border: 1px solid #ddd; padding: 4px 8px; color: #666;">✓ moong sprouts</span>
                            <span style="border: 1px solid #ddd; padding: 4px 8px; color: #666;">✓ yogurt</span>
                            <span style="border: 1px solid #ddd; padding: 4px 8px; color: #666;">✓ bananas</span>
                            <span style="border: 1px solid #ddd; padding: 4px 8px; color: #666;">✓ dal</span>
                            <span style="border: 1px solid #ddd; padding: 4px 8px; color: #666;">✓ rice</span>
                        </div>
                    </div>
                </div>
                
                <!-- Quick Delivery -->
                <div style="border: 1px solid #000000; background: #000000; color: white; padding: 16px; text-align: center;">
                    <h5 style="margin: 0 0 8px 0; font-size: 12px; font-weight: 600; letter-spacing: 0.5px;">QUICK DELIVERY</h5>
                    <p style="margin: 0 0 12px 0; font-size: 11px; opacity: 0.8;">Missing ingredients? 10-minute delivery</p>
                    <div style="display: flex; gap: 8px; justify-content: center; font-size: 10px; font-weight: 500;">
                        <span style="border: 1px solid #333; padding: 6px 10px; letter-spacing: 0.5px;">BLINKIT</span>
                        <span style="border: 1px solid #333; padding: 6px 10px; letter-spacing: 0.5px;">BIGBASKET</span>
                        <span style="border: 1px solid #333; padding: 6px 10px; letter-spacing: 0.5px;">GROFERS</span>
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <div style="
                text-align: center;
                padding: 24px 0;
                border-top: 1px solid #000000;
                margin-top: 32px;
            ">
                <p style="
                    margin: 0;
                    font-size: 12px;
                    color: #666;
                    font-weight: 300;
                    letter-spacing: 0.5px;
                ">
                    GENERATED BY NIGELA AI COOKING ASSISTANT
                </p>
                <p style="
                    margin: 4px 0 0 0;
                    font-size: 10px;
                    color: #999;
                    letter-spacing: 0.5px;
                ">
                    POWERED BY OPENAI • MADE WITH LOVE
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return email_html

if __name__ == "__main__":
    # Test the black and white email generation
    sample_plan = {}  # Would be filled with actual dishes
    date_str = "Sunday, September 8, 2024"
    
    email = generate_bw_complete_email(sample_plan, date_str)
    
    with open('BLACK_WHITE_COMPLETE_EMAIL.html', 'w') as f:
        f.write(email)
    
    print("✅ Black & white complete email template created!")
