"""
Curated YouTube Integration with Quality Channels
Features channels like Happy Pear, Ranveer Brar, Tarla Dalal, Satvic Movement
"""

import urllib.parse
from typing import Dict, List, Optional

# Curated YouTube channels for quality recipe content
PREMIUM_YOUTUBE_CHANNELS = {
    'happy_pear_vegan': {
        'name': 'The Happy Pear',
        'focus': 'Energetic vegan cooking, plant-based nutrition',
        'search_prefix': 'happy pear vegan',
        'specialties': ['vegan', 'healthy', 'energetic', 'plant_based', 'smoothie', 'bowl'],
        'style': 'Fun, energetic, health-focused'
    },
    'chef_ranveer_brar': {
        'name': 'Chef Ranveer Brar',
        'focus': 'Authentic Indian cuisine, professional techniques',
        'search_prefix': 'chef ranveer brar',
        'specialties': ['indian', 'authentic', 'professional', 'traditional', 'curry', 'dal'],
        'style': 'Professional, authentic, detailed technique'
    },
    'tarla_dalal': {
        'name': 'Tarla Dalal',
        'focus': 'Traditional Indian vegetarian, family recipes',
        'search_prefix': 'tarla dalal recipe',
        'specialties': ['traditional', 'vegetarian', 'family', 'gujarati', 'indian_sweets'],
        'style': 'Traditional, family-oriented, time-tested'
    },
    'satvic_movement': {
        'name': 'Satvic Movement',
        'focus': 'Satvik living, natural healing foods',
        'search_prefix': 'satvic movement',
        'specialties': ['satvik', 'healing', 'natural', 'ayurvedic', 'detox', 'immunity'],
        'style': 'Holistic, healing-focused, natural'
    },
    'bong_eats': {
        'name': 'Bong Eats',
        'focus': 'Bengali cuisine, regional Indian specialties',
        'search_prefix': 'bong eats vegetarian',
        'specialties': ['bengali', 'regional', 'authentic', 'cultural', 'traditional'],
        'style': 'Cultural, authentic, regional expertise'
    },
    'rajshri_food': {
        'name': 'Rajshri Food',
        'focus': 'Home-style Indian cooking, practical recipes',
        'search_prefix': 'rajshri food',
        'specialties': ['home_style', 'practical', 'indian', 'everyday', 'simple'],
        'style': 'Home-style, practical, everyday cooking'
    },
    'kabitas_kitchen': {
        'name': 'Kabita\'s Kitchen',
        'focus': 'Healthy Indian cooking, Odia specialties',
        'search_prefix': 'kabitas kitchen healthy',
        'specialties': ['healthy', 'odia', 'nutritious', 'regional', 'wellness'],
        'style': 'Health-conscious, regional, nutritious'
    },
    'cook_with_parul': {
        'name': 'Cook with Parul',
        'focus': 'Gujarati cuisine, traditional methods',
        'search_prefix': 'cook with parul gujarati',
        'specialties': ['gujarati', 'traditional', 'authentic', 'home_style'],
        'style': 'Gujarati expertise, traditional methods'
    },
    'hebbar_kitchen': {
        'name': 'Hebbar\'s Kitchen',
        'focus': 'South Indian cuisine, step-by-step tutorials',
        'search_prefix': 'hebbars kitchen',
        'specialties': ['south_indian', 'tutorial', 'detailed', 'traditional'],
        'style': 'Detailed tutorials, South Indian expertise'
    },
    'nisha_madhulika': {
        'name': 'Nisha Madhulika',
        'focus': 'Hindi cooking tutorials, North Indian cuisine',
        'search_prefix': 'nisha madhulika',
        'specialties': ['hindi', 'north_indian', 'tutorial', 'detailed'],
        'style': 'Hindi tutorials, detailed explanations'
    },
    'dr_vegan': {
        'name': 'Dr. Vegan',
        'focus': 'Plant-based nutrition, healthy vegan recipes',
        'search_prefix': 'dr vegan recipe',
        'specialties': ['vegan', 'healthy', 'nutrition', 'plant_based', 'quinoa', 'superfood'],
        'style': 'Science-backed vegan nutrition'
    },
    'sarah_vegan_kitchen': {
        'name': 'Sarah\'s Vegan Kitchen',
        'focus': 'Creative vegan cooking, plant-based comfort food',
        'search_prefix': 'sarah vegan kitchen',
        'specialties': ['vegan', 'creative', 'comfort_food', 'plant_based', 'innovative'],
        'style': 'Creative vegan comfort cooking'
    },
    'plant_you': {
        'name': 'PlantYou',
        'focus': 'Simple plant-based recipes, meal prep',
        'search_prefix': 'plantyou vegan recipe',
        'specialties': ['vegan', 'simple', 'meal_prep', 'plant_based', 'healthy', 'batch_cooking'],
        'style': 'Simple, accessible plant-based cooking'
    }
}

def select_best_youtube_channel(recipe_name: str, cuisine_hint: str = None, cooking_style: str = None) -> Dict:
    """Select the best YouTube channel for a specific recipe"""
    
    recipe_lower = recipe_name.lower()
    cuisine_lower = (cuisine_hint or '').lower()
    
    # Channel matching logic
    channel_scores = {}
    
    for channel_key, channel_data in PREMIUM_YOUTUBE_CHANNELS.items():
        score = 0
        specialties = channel_data['specialties']
        
        # Recipe name matching
        for specialty in specialties:
            if specialty in recipe_lower:
                score += 3
        
        # Cuisine matching
        if cuisine_hint:
            for specialty in specialties:
                if specialty in cuisine_lower:
                    score += 2
        
        # Special preferences
        if 'vegan' in recipe_lower or 'plant' in recipe_lower:
            if 'vegan' in specialties:
                score += 5
        
        if 'gujarati' in recipe_lower or 'thepla' in recipe_lower or 'dhokla' in recipe_lower:
            if 'gujarati' in specialties:
                score += 5
        
        if 'south' in cuisine_lower or any(word in recipe_lower for word in ['dosa', 'idli', 'sambhar', 'rasam']):
            if 'south_indian' in specialties:
                score += 5
        
        if 'healthy' in recipe_lower or 'quinoa' in recipe_lower or 'superfood' in recipe_lower:
            if 'healthy' in specialties or 'satvik' in specialties:
                score += 4
        
        channel_scores[channel_key] = score
    
    # Select best channel
    best_channel_key = max(channel_scores, key=channel_scores.get)
    best_channel = PREMIUM_YOUTUBE_CHANNELS[best_channel_key]
    
    return best_channel

def get_curated_youtube_url(recipe_name: str, cuisine_hint: str = None) -> tuple[str, str]:
    """Get curated YouTube URL and channel name"""
    
    best_channel = select_best_youtube_channel(recipe_name, cuisine_hint)
    
    # Construct search query
    search_query = f"{best_channel['search_prefix']} {recipe_name} recipe"
    youtube_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(search_query)}"
    
    return youtube_url, best_channel['name']

def generate_youtube_section_html(recipes: List[tuple]) -> str:
    """Generate HTML section with curated YouTube links"""
    
    html = '''
    <div style="border: 1px solid #000; margin-bottom: 20px; background: white;">
        <div style="background: #000; color: white; padding: 15px; text-align: center;">
            <h3 style="margin: 0; font-size: 14px; letter-spacing: 1px;">CURATED YOUTUBE VIDEOS</h3>
            <p style="margin: 4px 0 0 0; font-size: 10px; opacity: 0.8;">From premium cooking channels</p>
        </div>
        <div style="padding: 15px;">
    '''
    
    for recipe_name, cuisine_hint, meal_type in recipes:
        youtube_url, channel_name = get_curated_youtube_url(recipe_name, cuisine_hint)
        
        html += f'''
            <div style="margin-bottom: 8px; font-size: 11px;">
                <a href="{youtube_url}" target="_blank" style="color: #000; text-decoration: none; font-weight: 500;">
                    ▶ {recipe_name}
                </a>
                <span style="color: #666; font-size: 10px;"> • {channel_name}</span>
            </div>
        '''
    
    html += '''
        </div>
        <div style="background: #f8f8f8; padding: 10px; text-align: center; font-size: 10px; color: #666;">
            Curated from: Happy Pear • Ranveer Brar • Tarla Dalal • Satvic Movement • More
        </div>
    </div>
    '''
    
    return html

if __name__ == "__main__":
    # Test curated YouTube integration
    test_recipes = [
        ('Quinoa Buddha Bowl', 'healthy', 'lunch'),
        ('Gujarati Dal', 'gujarati', 'lunch'),
        ('Green Smoothie', 'vegan', 'breakfast'),
        ('Masoor Dal Curry', 'indian', 'lunch')
    ]
    
    print("🎥 TESTING CURATED YOUTUBE INTEGRATION")
    print("=" * 50)
    
    for recipe, cuisine, meal in test_recipes:
        url, channel = get_curated_youtube_url(recipe, cuisine)
        print(f"🍽️ {recipe} ({cuisine})")
        print(f"   📺 Channel: {channel}")
        print(f"   🔗 URL: {url[:60]}...")
        print()
    
    print("✅ Curated YouTube system ready!")
