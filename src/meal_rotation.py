"""
Advanced Meal Rotation System for Nigela
Ensures variety, follows structure preferences, prevents repetition
"""

from datetime import datetime, timedelta
from typing import Dict, List, Set
import json
import random
from pathlib import Path

class MealRotationManager:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.history_file = self.data_dir / "meal_history.json"
        self.load_history()
        
        # Meal structure templates
        self.meal_structures = {
            'traditional_thali': {
                'lunch': ['dal', 'vegetable', 'rice', 'roti', 'salad'],
                'dinner': ['soup_light', 'khichdi', 'pickle']
            },
            'modern_healthy': {
                'lunch': ['protein_bowl', 'grain_bowl', 'vegetable', 'bread'],
                'dinner': ['soup', 'light_curry', 'millet_bread']
            },
            'surprise_fusion': {
                'lunch': ['healthy_burger', 'sweet_potato_fries', 'green_salad'],
                'dinner': ['asian_soup', 'quinoa_bowl', 'herbal_tea']
            },
            'festival_special': {
                'lunch': ['special_dal', 'festive_vegetable', 'pulao', 'puri', 'raita'],
                'dinner': ['light_kheer', 'digestive_tea']
            }
        }
        
        # Rotation categories with 2-week variety
        self.rotation_items = {
            'dal': [
                'toor_dal_gujarati', 'masoor_dal_tadka', 'moong_dal_simple', 'chana_dal_spicy',
                'mixed_dal', 'spinach_dal', 'bottle_gourd_dal', 'tomato_dal',
                'coconut_dal_south', 'rajasthani_dal', 'bengali_dal', 'punjabi_dal',
                'quinoa_dal_fusion', 'red_kidney_bean_curry'
            ],
            'roti_flour': [
                'wheat_phulka', 'bajra_roti', 'jowar_roti', 'ragi_roti',
                'methi_thepla', 'palak_paratha', 'beetroot_paratha', 'carrot_paratha',
                'multigrain_roti', 'oats_roti', 'quinoa_roti', 'amaranth_roti',
                'stuffed_aloo_paratha', 'stuffed_gobi_paratha'
            ],
            'khichdi': [
                'moong_dal_khichdi', 'quinoa_khichdi', 'bajra_khichdi', 'vegetable_khichdi',
                'masoor_khichdi', 'mixed_millet_khichdi', 'spinach_khichdi', 'tomato_khichdi',
                'coconut_khichdi', 'lemon_khichdi', 'curry_leaf_khichdi', 'ginger_khichdi'
            ],
            'vegetables': [
                'bharela_ringna', 'aloo_gobi', 'bhindi_masala', 'lauki_curry',
                'turai_sabzi', 'karela_fry', 'baingan_bharta', 'palak_paneer',
                'matar_paneer', 'mixed_vegetable_curry', 'cabbage_poriyal', 'beans_poriyal',
                'drumstick_curry', 'ridge_gourd_dal', 'bottle_gourd_kofta'
            ],
            'rice': [
                'plain_basmati', 'jeera_rice', 'lemon_rice', 'coconut_rice',
                'vegetable_pulao', 'quinoa_pilaf', 'brown_rice', 'red_rice',
                'turmeric_rice', 'mint_rice', 'tomato_rice', 'curd_rice'
            ],
            'surprise_items': [
                'quinoa_veggie_burger', 'millet_pizza_base', 'healthy_pasta_salad',
                'stuffed_bell_peppers', 'zucchini_noodles', 'cauliflower_steaks',
                'sweet_potato_gnocchi', 'beetroot_hummus_wrap', 'avocado_toast_indian'
            ]
        }
        
    def load_history(self):
        """Load meal history from JSON file"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            else:
                self.history = {
                    'last_14_days': [],
                    'last_used_dates': {},
                    'weekly_structure_count': {}
                }
        except Exception:
            self.history = {
                'last_14_days': [],
                'last_used_dates': {},
                'weekly_structure_count': {}
            }
    
    def save_history(self):
        """Save meal history to JSON file"""
        self.data_dir.mkdir(exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2, default=str)
    
    def get_available_items(self, category: str, exclude_days: int = 14) -> List[str]:
        """Get items not used in the last N days"""
        cutoff_date = datetime.now() - timedelta(days=exclude_days)
        
        recently_used = set()
        for day_data in self.history['last_14_days']:
            if datetime.fromisoformat(day_data['date']) > cutoff_date:
                for meal_items in day_data.get('meals', {}).values():
                    for item in meal_items:
                        if item.get('category') == category:
                            recently_used.add(item.get('name'))
        
        available = [item for item in self.rotation_items[category] if item not in recently_used]
        
        # If all items used recently, reset with least recently used
        if not available:
            available = self.rotation_items[category][:3]  # Use first 3 as fallback
            
        return available
    
    def select_meal_structure(self, day_of_week: int) -> str:
        """Select meal structure based on day and variety"""
        structures = list(self.meal_structures.keys())
        
        # Traditional most days, surprises occasionally
        if day_of_week in [0, 2, 4]:  # Monday, Wednesday, Friday
            return 'traditional_thali'
        elif day_of_week in [1, 3]:  # Tuesday, Thursday  
            return 'modern_healthy'
        elif day_of_week == 5:  # Saturday - surprise day
            return 'surprise_fusion'
        else:  # Sunday - special day
            return 'festival_special'
    
    def generate_daily_plan(self, target_date: datetime = None) -> Dict:
        """Generate daily meal plan with variety and structure"""
        if not target_date:
            target_date = datetime.now() + timedelta(days=1)
        
        day_of_week = target_date.weekday()
        structure_type = self.select_meal_structure(day_of_week)
        structure = self.meal_structures[structure_type]
        
        daily_plan = {
            'date': target_date.isoformat(),
            'structure_type': structure_type,
            'meals': {}
        }
        
        # Generate breakfast (always similar structure)
        daily_plan['meals']['breakfast'] = {
            'main_starch': self._select_breakfast_starch(),
            'protein': self._select_breakfast_protein(),
            'dairy': self._select_breakfast_dairy(),
            'fruit': self._select_breakfast_fruit()
        }
        
        # Generate snacks
        daily_plan['meals']['morning_snack'] = {
            'item': self._select_healthy_snack('morning')
        }
        
        daily_plan['meals']['evening_snack'] = {
            'item': self._select_healthy_snack('evening')
        }
        
        # Generate lunch based on structure
        if 'lunch' in structure:
            daily_plan['meals']['lunch'] = {}
            for slot in structure['lunch']:
                if slot == 'dal':
                    available_dals = self.get_available_items('dal')
                    daily_plan['meals']['lunch']['dal'] = {
                        'name': random.choice(available_dals),
                        'category': 'dal'
                    }
                elif slot == 'roti':
                    available_rotis = self.get_available_items('roti_flour')
                    daily_plan['meals']['lunch']['roti'] = {
                        'name': random.choice(available_rotis),
                        'category': 'roti_flour'
                    }
                elif slot == 'rice':
                    available_rice = self.get_available_items('rice')
                    daily_plan['meals']['lunch']['rice'] = {
                        'name': random.choice(available_rice),
                        'category': 'rice'
                    }
                elif slot == 'vegetable':
                    available_veg = self.get_available_items('vegetables')
                    daily_plan['meals']['lunch']['vegetable'] = {
                        'name': random.choice(available_veg),
                        'category': 'vegetables'
                    }
                elif slot == 'salad':
                    daily_plan['meals']['lunch']['salad'] = {
                        'name': 'fresh_seasonal_salad',
                        'category': 'salad'
                    }
                elif slot in ['healthy_burger', 'protein_bowl']:
                    available_surprise = self.get_available_items('surprise_items')
                    daily_plan['meals']['lunch'][slot] = {
                        'name': random.choice(available_surprise),
                        'category': 'surprise_items'
                    }
        
        # Generate dinner based on structure
        if 'dinner' in structure:
            daily_plan['meals']['dinner'] = {}
            for slot in structure['dinner']:
                if slot == 'khichdi':
                    available_khichdi = self.get_available_items('khichdi')
                    daily_plan['meals']['dinner']['khichdi'] = {
                        'name': random.choice(available_khichdi),
                        'category': 'khichdi'
                    }
                elif slot in ['soup_light', 'soup']:
                    daily_plan['meals']['dinner']['soup'] = {
                        'name': self._select_soup(),
                        'category': 'soup'
                    }
        
        # Update history
        self.history['last_14_days'].append(daily_plan)
        
        # Keep only last 14 days
        cutoff_date = datetime.now() - timedelta(days=14)
        self.history['last_14_days'] = [
            day for day in self.history['last_14_days']
            if datetime.fromisoformat(day['date']) > cutoff_date
        ]
        
        self.save_history()
        return daily_plan
    
    def _select_breakfast_starch(self):
        return random.choice(['dosa_variety', 'upma_variety', 'paratha_variety', 'pancake_healthy'])
    
    def _select_breakfast_protein(self):
        return random.choice(['sprout_salad', 'besan_chilla', 'paneer_scramble', 'tofu_bhurji'])
    
    def _select_breakfast_dairy(self):
        return random.choice(['plain_yogurt', 'flavored_lassi', 'buttermilk', 'coconut_yogurt'])
    
    def _select_breakfast_fruit(self):
        return random.choice(['seasonal_fruit_bowl', 'fruit_chaat', 'smoothie_bowl', 'fruit_salad'])
    
    def _select_healthy_snack(self, time):
        if time == 'morning':
            return random.choice(['fruit_bowl', 'nuts_dates', 'green_smoothie', 'herbal_tea'])
        else:
            return random.choice(['masala_chai', 'herbal_tea', 'roasted_chana', 'fruit_chaat'])
    
    def _select_soup(self):
        return random.choice(['tomato_basil', 'pumpkin_ginger', 'spinach_coconut', 'mixed_vegetable'])

# YouTube channel integration
CURATED_YOUTUBE_CHANNELS = {
    'happy_pear': {
        'channel': 'The Happy Pear',
        'focus': 'Vegan, healthy, energetic cooking',
        'search_prefix': 'happy pear vegan'
    },
    'ranveer_brar': {
        'channel': 'Chef Ranveer Brar',
        'focus': 'Authentic Indian cuisine, professional techniques',
        'search_prefix': 'chef ranveer brar'
    },
    'tarla_dalal': {
        'channel': 'Tarla Dalal',
        'focus': 'Traditional Indian vegetarian recipes',
        'search_prefix': 'tarla dalal recipe'
    },
    'satvic_movement': {
        'channel': 'Satvic Movement',
        'focus': 'Satvik, natural, healing foods',
        'search_prefix': 'satvic movement recipe'
    },
    'bong_eats': {
        'channel': 'Bong Eats',
        'focus': 'Bengali vegetarian specialties',
        'search_prefix': 'bong eats vegetarian'
    },
    'rajshri_food': {
        'channel': 'Rajshri Food',
        'focus': 'Traditional Indian home cooking',
        'search_prefix': 'rajshri food vegetarian'
    },
    'kabitas_kitchen': {
        'channel': 'Kabita\'s Kitchen',
        'focus': 'Healthy Indian cooking, regional specialties',
        'search_prefix': 'kabitas kitchen healthy'
    },
    'cook_with_parul': {
        'channel': 'Cook with Parul',
        'focus': 'Gujarati and Indian vegetarian',
        'search_prefix': 'cook with parul gujarati'
    }
}

def get_curated_youtube_link(recipe_name: str, cuisine_hint: str = None) -> str:
    """Get YouTube link with curated channel preference"""
    
    # Match recipe to best channel
    recipe_lower = recipe_name.lower()
    
    if any(word in recipe_lower for word in ['gujarati', 'thepla', 'dhokla', 'bharela']):
        channel = CURATED_YOUTUBE_CHANNELS['cook_with_parul']
    elif any(word in recipe_lower for word in ['healthy', 'quinoa', 'superfood', 'bowl']):
        channel = CURATED_YOUTUBE_CHANNELS['satvic_movement']
    elif any(word in recipe_lower for word in ['vegan', 'plant', 'green']):
        channel = CURATED_YOUTUBE_CHANNELS['happy_pear']
    elif any(word in recipe_lower for word in ['traditional', 'authentic', 'classic']):
        channel = CURATED_YOUTUBE_CHANNELS['tarla_dalal']
    elif any(word in recipe_lower for word in ['professional', 'restaurant', 'chef']):
        channel = CURATED_YOUTUBE_CHANNELS['ranveer_brar']
    else:
        # Default to Rajshri Food for general Indian recipes
        channel = CURATED_YOUTUBE_CHANNELS['rajshri_food']
    
    # Construct search URL with channel preference
    import urllib.parse
    search_query = f"{channel['search_prefix']} {recipe_name}"
    return f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(search_query)}"

def generate_weekly_meal_plan(start_date: datetime = None) -> List[Dict]:
    """Generate complete weekly meal plan with variety"""
    if not start_date:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    manager = MealRotationManager()
    weekly_plan = []
    
    for day in range(7):
        target_date = start_date + timedelta(days=day)
        daily_plan = manager.generate_daily_plan(target_date)
        weekly_plan.append(daily_plan)
    
    return weekly_plan

if __name__ == "__main__":
    # Test the rotation system
    print("🔄 TESTING MEAL ROTATION SYSTEM")
    print("=" * 50)
    
    manager = MealRotationManager()
    
    # Test daily plan generation
    today = datetime.now()
    plan = manager.generate_daily_plan(today)
    
    print(f"📅 Date: {plan['date']}")
    print(f"🏗️ Structure: {plan['structure_type']}")
    print()
    
    for meal, items in plan['meals'].items():
        print(f"{meal.upper()}:")
        for slot, item in items.items():
            if isinstance(item, dict):
                print(f"  {slot}: {item['name']} ({item['category']})")
            else:
                print(f"  {slot}: {item}")
    
    print()
    print("✅ Meal rotation system ready!")
    print("🎥 YouTube channel curation configured!")
    print("📊 2-week variety tracking implemented!")
