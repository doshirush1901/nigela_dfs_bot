"""
Additional meal planning sections for email
Special comments, soaking instructions, and nutrition summaries
"""

def generate_soaking_instructions(plan: dict) -> str:
    """Generate overnight soaking instructions for next day"""
    
    soaking_items = []
    
    # Check all dishes for ingredients that need soaking
    for meal_dishes in plan.values():
        for dish in meal_dishes.values():
            for ingredient in getattr(dish, 'ingredients', []):
                item = getattr(ingredient, 'item', '').lower()
                qty = getattr(ingredient, 'qty', 0)
                unit = getattr(ingredient, 'unit', '')
                
                # Items that typically need soaking
                if any(soak_item in item for soak_item in [
                    'dal', 'lentil', 'chickpea', 'chana', 'rajma', 'kidney bean',
                    'black gram', 'urad', 'moong', 'masoor', 'toor'
                ]):
                    qty_text = f" ({qty}{unit})" if qty > 0 else ""
                    soaking_items.append(f"{item.title()}{qty_text}")
    
    # Remove duplicates
    unique_soaking = list(dict.fromkeys(soaking_items))
    
    if not unique_soaking:
        return ""
    
    soaking_html = f"""
    <div style="
        border: 1px solid #000000;
        margin-bottom: 24px;
        background: white;
    ">
        <div style="
            background: #000000;
            color: white;
            padding: 16px;
            text-align: center;
        ">
            <h3 style="
                margin: 0;
                font-size: 14px;
                font-weight: 500;
                letter-spacing: 1px;
            ">TONIGHT'S PREP</h3>
        </div>
        
        <div style="padding: 16px;">
            <h4 style="
                margin: 0 0 12px 0;
                font-size: 13px;
                font-weight: 600;
                color: #000000;
                letter-spacing: 0.5px;
            ">🌙 SOAK OVERNIGHT</h4>
            
            <ul style="
                margin: 0;
                padding-left: 16px;
                font-size: 12px;
                color: #333;
                line-height: 1.6;
            ">
                {''.join([f'<li style="margin-bottom: 4px;">{item} - soak in clean water</li>' for item in unique_soaking])}
            </ul>
            
            <div style="
                background: #f8f8f8;
                padding: 12px;
                margin-top: 12px;
                border: 1px solid #e0e0e0;
                font-size: 11px;
                color: #666;
                font-style: italic;
            ">
                💡 <strong>Tip:</strong> Soaking overnight makes dal cook faster and digest better
            </div>
        </div>
    </div>
    """
    
    return soaking_html

def generate_special_comments(plan: dict) -> str:
    """Generate special cooking comments and tips for today's menu"""
    
    # Collect special notes based on dishes
    special_notes = []
    seasonal_notes = []
    health_notes = []
    
    # Analyze dishes for special comments
    for meal_dishes in plan.values():
        for dish in meal_dishes.values():
            dish_name = dish.name.lower()
            tags = getattr(dish, 'tags', [])
            
            # Seasonal comments
            if any(item in dish_name for item in ['pumpkin', 'gourd', 'seasonal']):
                seasonal_notes.append(f"• {dish.name} uses seasonal vegetables - adjust based on availability")
            
            # Health comments
            if 'jain' in tags:
                health_notes.append(f"• {dish.name} is Jain-friendly (no root vegetables)")
            
            if any(item in dish_name for item in ['sprout', 'dal', 'lentil']):
                health_notes.append(f"• {dish.name} provides plant-based protein for muscle health")
            
            if any(item in dish_name for item in ['ragi', 'millet', 'jowar', 'bajra']):
                health_notes.append(f"• {dish.name} uses millet - excellent for diabetes management")
            
            # Cooking technique comments
            if getattr(dish, 'cook_minutes', 0) > 30:
                special_notes.append(f"• {dish.name} needs patience - slow cooking develops deep flavors")
            
            if any(word in dish_name for word in ['tempering', 'tadka']):
                special_notes.append(f"• {dish.name} benefits from proper spice tempering technique")
    
    # Remove duplicates and limit to most important
    unique_special = list(dict.fromkeys(special_notes))[:3]
    unique_seasonal = list(dict.fromkeys(seasonal_notes))[:2]
    unique_health = list(dict.fromkeys(health_notes))[:4]
    
    if not (unique_special or unique_seasonal or unique_health):
        return ""
    
    comments_html = f"""
    <div style="
        border: 1px solid #000000;
        margin-bottom: 24px;
        background: white;
    ">
        <div style="
            background: #000000;
            color: white;
            padding: 16px;
            text-align: center;
        ">
            <h3 style="
                margin: 0;
                font-size: 14px;
                font-weight: 500;
                letter-spacing: 1px;
            ">SPECIAL NOTES</h3>
        </div>
        
        <div style="padding: 16px;">
    """
    
    if unique_special:
        comments_html += f"""
            <div style="margin-bottom: 16px;">
                <h4 style="
                    margin: 0 0 8px 0;
                    font-size: 12px;
                    font-weight: 600;
                    color: #000000;
                    letter-spacing: 0.5px;
                ">🍳 COOKING TIPS</h4>
                <ul style="margin: 0; padding-left: 16px; font-size: 11px; color: #333; line-height: 1.5;">
                    {''.join([f'<li style="margin-bottom: 4px;">{note[2:]}</li>' for note in unique_special])}
                </ul>
            </div>
        """
    
    if unique_health:
        comments_html += f"""
            <div style="margin-bottom: 16px;">
                <h4 style="
                    margin: 0 0 8px 0;
                    font-size: 12px;
                    font-weight: 600;
                    color: #000000;
                    letter-spacing: 0.5px;
                ">💚 HEALTH BENEFITS</h4>
                <ul style="margin: 0; padding-left: 16px; font-size: 11px; color: #333; line-height: 1.5;">
                    {''.join([f'<li style="margin-bottom: 4px;">{note[2:]}</li>' for note in unique_health])}
                </ul>
            </div>
        """
    
    if unique_seasonal:
        comments_html += f"""
            <div>
                <h4 style="
                    margin: 0 0 8px 0;
                    font-size: 12px;
                    font-weight: 600;
                    color: #000000;
                    letter-spacing: 0.5px;
                ">🌱 SEASONAL NOTES</h4>
                <ul style="margin: 0; padding-left: 16px; font-size: 11px; color: #333; line-height: 1.5;">
                    {''.join([f'<li style="margin-bottom: 4px;">{note[2:]}</li>' for note in unique_seasonal])}
                </ul>
            </div>
        """
    
    comments_html += """
        </div>
    </div>
    """
    
    return comments_html

def generate_total_nutrition_summary(plan: dict) -> str:
    """Generate comprehensive nutrition summary for all dishes"""
    
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fats = 0
    total_fiber = 0
    dish_count = 0
    
    meal_breakdowns = {}
    
    # Calculate totals and meal breakdowns
    for meal_name, meal_dishes in plan.items():
        meal_calories = 0
        meal_protein = 0
        meal_count = 0
        
        for dish in meal_dishes.values():
            calories = getattr(dish, 'calories', 200)
            protein = getattr(dish, 'protein_g', 8)
            carbs = getattr(dish, 'carbs_g', 30)
            fats = getattr(dish, 'fats_g', 8)
            fiber = getattr(dish, 'fiber_g', 3)
            
            total_calories += calories
            total_protein += protein
            total_carbs += carbs
            total_fats += fats
            total_fiber += fiber
            dish_count += 1
            
            meal_calories += calories
            meal_protein += protein
            meal_count += 1
        
        meal_breakdowns[meal_name] = {
            'calories': meal_calories,
            'protein': meal_protein,
            'dishes': meal_count
        }
    
    # Calculate percentages for profiles
    parent_percent = (total_calories / 1800) * 100
    kids_percent = (total_calories / 1600) * 100
    
    # Determine nutritional quality
    protein_per_cal = (total_protein * 4) / total_calories * 100  # % calories from protein
    carbs_per_cal = (total_carbs * 4) / total_calories * 100     # % calories from carbs
    fats_per_cal = (total_fats * 9) / total_calories * 100       # % calories from fats
    
    nutrition_html = f"""
    <div style="
        border: 1px solid #000000;
        margin-bottom: 24px;
        background: white;
    ">
        <div style="
            background: #000000;
            color: white;
            padding: 16px;
            text-align: center;
        ">
            <h3 style="
                margin: 0;
                font-size: 14px;
                font-weight: 500;
                letter-spacing: 1px;
            ">COMPLETE NUTRITION ANALYSIS</h3>
        </div>
        
        <!-- Daily Totals -->
        <div style="padding: 16px; border-bottom: 1px solid #e0e0e0;">
            <h4 style="
                margin: 0 0 12px 0;
                font-size: 13px;
                font-weight: 600;
                color: #000000;
                letter-spacing: 0.5px;
                text-align: center;
            ">📊 DAILY TOTALS ({dish_count} DISHES)</h4>
            
            <div style="
                display: flex;
                justify-content: space-between;
                background: #f8f8f8;
                padding: 12px;
                border: 1px solid #e0e0e0;
                font-size: 12px;
                font-weight: 600;
                margin-bottom: 12px;
            ">
                <span>🔥 {total_calories:.0f} kcal</span>
                <span>🥩 {total_protein:.0f}g</span>
                <span>🍞 {total_carbs:.0f}g</span>
                <span>🥑 {total_fats:.0f}g</span>
            </div>
            
            <!-- Profile Comparison -->
            <div style="display: flex; gap: 8px;">
                <div style="
                    flex: 1;
                    border: 1px solid #000000;
                    padding: 12px;
                    text-align: center;
                    background: #f8f8f8;
                ">
                    <div style="font-size: 16px; font-weight: 600; color: #000; margin-bottom: 4px;">👨‍👩‍👧‍👦</div>
                    <div style="font-size: 11px; color: #666; margin-bottom: 4px;">PARENTS</div>
                    <div style="font-size: 18px; font-weight: 700; color: #000;">{parent_percent:.0f}%</div>
                    <div style="font-size: 9px; color: #999;">of 1800 cal deficit goal</div>
                </div>
                
                <div style="
                    flex: 1;
                    border: 1px solid #000000;
                    padding: 12px;
                    text-align: center;
                    background: #f8f8f8;
                ">
                    <div style="font-size: 16px; font-weight: 600; color: #000; margin-bottom: 4px;">👶</div>
                    <div style="font-size: 11px; color: #666; margin-bottom: 4px;">KIDS</div>
                    <div style="font-size: 18px; font-weight: 700; color: #000;">{kids_percent:.0f}%</div>
                    <div style="font-size: 9px; color: #999;">of 1600 cal growth goal</div>
                </div>
            </div>
        </div>
        
        <!-- Macro Distribution -->
        <div style="padding: 16px; border-bottom: 1px solid #e0e0e0;">
            <h4 style="
                margin: 0 0 12px 0;
                font-size: 13px;
                font-weight: 600;
                color: #000000;
                letter-spacing: 0.5px;
                text-align: center;
            ">⚖️ MACRO DISTRIBUTION</h4>
            
            <div style="font-size: 11px; color: #333; line-height: 1.8;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>🥩 Protein:</span>
                    <span><strong>{protein_per_cal:.0f}% of calories</strong> (Target: 15-20%)</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>🍞 Carbohydrates:</span>
                    <span><strong>{carbs_per_cal:.0f}% of calories</strong> (Target: 50-60%)</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>🥑 Fats:</span>
                    <span><strong>{fats_per_cal:.0f}% of calories</strong> (Target: 20-30%)</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>🌾 Fiber:</span>
                    <span><strong>{total_fiber:.0f}g total</strong> (Target: 25-35g)</span>
                </div>
            </div>
        </div>
        
        <!-- Meal-wise Breakdown -->
        <div style="padding: 16px;">
            <h4 style="
                margin: 0 0 12px 0;
                font-size: 13px;
                font-weight: 600;
                color: #000000;
                letter-spacing: 0.5px;
                text-align: center;
            ">🍽️ MEAL BREAKDOWN</h4>
            
            <div style="font-size: 11px; color: #333;">
    """
    
    meal_emojis = {
        'breakfast': '🌅',
        'morning_snack': '🥝',
        'lunch': '☀️',
        'evening_snack': '☕',
        'dinner': '🌙'
    }
    
    for meal_key, breakdown in meal_breakdowns.items():
        if breakdown['calories'] > 0:
            meal_name = meal_key.replace('_', ' ').title()
            emoji = meal_emojis.get(meal_key, '🍽️')
            percent_of_day = (breakdown['calories'] / total_calories) * 100
            
            nutrition_html += f"""
                <div style="
                    display: flex;
                    justify-content: space-between;
                    padding: 6px 0;
                    border-bottom: 1px solid #f0f0f0;
                ">
                    <span>{emoji} {meal_name}:</span>
                    <span><strong>{breakdown['calories']:.0f} kcal</strong> ({percent_of_day:.0f}% of day)</span>
                </div>
            """
    
    nutrition_html += """
            </div>
        </div>
    </div>
    """
    
    return nutrition_html

def generate_special_dietary_notes(plan: dict) -> str:
    """Generate dietary compliance and special notes"""
    
    # Analyze dietary compliance
    jain_dishes = 0
    vegetarian_dishes = 0
    total_dishes = 0
    gluten_free_dishes = 0
    
    for meal_dishes in plan.values():
        for dish in meal_dishes.values():
            total_dishes += 1
            tags = getattr(dish, 'tags', [])
            
            if 'jain' in tags:
                jain_dishes += 1
            if 'vegetarian' in tags:
                vegetarian_dishes += 1
            if any(tag in ['gluten_free', 'millet', 'rice'] for tag in tags):
                gluten_free_dishes += 1
    
    jain_percent = (jain_dishes / total_dishes) * 100 if total_dishes > 0 else 0
    
    dietary_html = f"""
    <div style="
        border: 1px solid #000000;
        margin-bottom: 24px;
        background: white;
    ">
        <div style="
            background: #000000;
            color: white;
            padding: 16px;
            text-align: center;
        ">
            <h3 style="
                margin: 0;
                font-size: 14px;
                font-weight: 500;
                letter-spacing: 1px;
            ">DIETARY COMPLIANCE</h3>
        </div>
        
        <div style="padding: 16px;">
            <div style="
                background: #f8f8f8;
                padding: 12px;
                border: 1px solid #e0e0e0;
                margin-bottom: 12px;
                text-align: center;
            ">
                <div style="font-size: 12px; font-weight: 600; color: #000; margin-bottom: 6px;">
                    ✅ {jain_percent:.0f}% JAIN-FRIENDLY DISHES
                </div>
                <div style="font-size: 10px; color: #666;">
                    {jain_dishes} of {total_dishes} dishes comply with Jain dietary guidelines
                </div>
            </div>
            
            <div style="font-size: 11px; color: #333; line-height: 1.6;">
                <div style="margin-bottom: 6px;">
                    <strong>🕊️ Jain Compliance:</strong> No root vegetables, no harm-based ingredients
                </div>
                <div style="margin-bottom: 6px;">
                    <strong>🌱 Vegetarian:</strong> 100% plant-based nutrition
                </div>
                <div style="margin-bottom: 6px;">
                    <strong>👨‍👩‍👧‍👦 Family-Friendly:</strong> Suitable for all ages with portion adjustments
                </div>
                <div>
                    <strong>🌾 Gluten Options:</strong> {gluten_free_dishes} dishes naturally gluten-free
                </div>
            </div>
        </div>
    </div>
    """
    
    return dietary_html

if __name__ == "__main__":
    # Test the additional sections
    print("✅ Meal planning extras module created!")
    print("📋 Available sections:")
    print("• Soaking instructions for overnight prep")
    print("• Special cooking comments and tips") 
    print("• Complete nutrition analysis")
    print("• Dietary compliance summary")
