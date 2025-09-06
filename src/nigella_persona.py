"""
Nigella Lawson-style Email Persona for Nigela
British dry humor, seasonal Mumbai commentary, food philosophy
Enhanced with Hindu/Jain calendar awareness and Ayurvedic wisdom
"""

import random
from datetime import datetime, date
from typing import Dict, List
import calendar

class NigellaPersona:
    def __init__(self):
        # Mumbai seasonal context
        self.mumbai_seasons = {
            'winter': {'months': [11, 12, 1, 2], 'name': 'Winter'},
            'summer': {'months': [3, 4, 5], 'name': 'Summer'}, 
            'monsoon': {'months': [6, 7, 8, 9, 10], 'name': 'Monsoon'}
        }
        
        # Hindu calendar festivals and food connections
        self.hindu_calendar = {
            1: {  # January
                'festivals': ['Makar Sankranti', 'Vasant Panchami'],
                'food_wisdom': 'Sesame and jaggery for warmth, yellow foods for Saraswati',
                'ayurvedic_note': 'Kapha season - light, warm, spiced foods'
            },
            2: {  # February  
                'festivals': ['Maha Shivratri'],
                'food_wisdom': 'Fasting foods, fruits, milk-based preparations',
                'ayurvedic_note': 'Late winter - digestive fire needs kindling'
            },
            3: {  # March
                'festivals': ['Holi', 'Chaitra Navratri begins'],
                'food_wisdom': 'Spring vegetables, detoxifying bitter greens',
                'ayurvedic_note': 'Transition season - cleansing, light foods'
            },
            4: {  # April
                'festivals': ['Ram Navami', 'Hanuman Jayanti'],
                'food_wisdom': 'Cooling foods as heat increases, fresh fruits',
                'ayurvedic_note': 'Pitta begins - reduce heating spices'
            },
            5: {  # May
                'festivals': ['Akshaya Tritiya'],
                'food_wisdom': 'Cooling drinks, coconut water, seasonal mangoes',
                'ayurvedic_note': 'Peak summer - cooling, hydrating foods essential'
            },
            6: {  # June
                'festivals': ['Ganga Dussehra', 'Rath Yatra'],
                'food_wisdom': 'Light foods for monsoon prep, digestive spices',
                'ayurvedic_note': 'Pre-monsoon - strengthen digestion'
            },
            7: {  # July
                'festivals': ['Guru Purnima'],
                'food_wisdom': 'Monsoon foods - warm, dry, well-spiced',
                'ayurvedic_note': 'Vata aggravation - avoid raw, cold foods'
            },
            8: {  # August
                'festivals': ['Raksha Bandhan', 'Krishna Janmashtami'],
                'food_wisdom': 'Festival sweets in moderation, milk-based dishes',
                'ayurvedic_note': 'Monsoon continues - ginger, turmeric essential'
            },
            9: {  # September
                'festivals': ['Ganesh Chaturthi', 'Navratri begins'],
                'food_wisdom': 'Fasting foods, seasonal vegetables, modaks',
                'ayurvedic_note': 'Post-monsoon - rebuild digestive strength'
            },
            10: {  # October
                'festivals': ['Dussehra', 'Karva Chauth'],
                'food_wisdom': 'Celebration foods, seasonal fruits, festival preparations',
                'ayurvedic_note': 'Ideal season - all foods in balance'
            },
            11: {  # November
                'festivals': ['Diwali', 'Govardhan Puja', 'Bhai Dooj'],
                'food_wisdom': 'Festival sweets, dry fruits, celebration meals',
                'ayurvedic_note': 'Vata season begins - warm, oily, nourishing foods'
            },
            12: {  # December
                'festivals': ['Gita Jayanti'],
                'food_wisdom': 'Winter warming foods, sesame, jaggery preparations',
                'ayurvedic_note': 'Peak winter - heavy, warm, sweet foods'
            }
        }
        
        # Jain calendar considerations
        self.jain_calendar = {
            'paryushan': {
                'months': [8, 9],  # Usually Aug-Sep
                'food_wisdom': 'Simple, pure foods. No root vegetables, minimal spices',
                'philosophy': 'Food as spiritual practice - simplicity and mindfulness'
            },
            'chaturmas': {
                'months': [6, 7, 8, 9],  # Monsoon months
                'food_wisdom': 'Avoid green vegetables, focus on dried/stored foods',
                'philosophy': 'Minimal harm to growing life during monsoon'
            },
            'ekadashi': {
                'frequency': 'twice_monthly',
                'food_wisdom': 'Fasting or single meal, fruits and milk',
                'philosophy': 'Digestive rest and spiritual focus'
            }
        }
        
        # Mumbai market seasonality
        self.mumbai_markets = {
            'winter': {
                'vegetables': ['cauliflower', 'cabbage', 'peas', 'carrots', 'spinach', 'methi'],
                'fruits': ['oranges', 'sweet lime', 'guava', 'pomegranate'],
                'specialties': 'Best time for leafy greens, winter gourds'
            },
            'summer': {
                'vegetables': ['bottle gourd', 'ridge gourd', 'cucumber', 'okra'],
                'fruits': ['mango', 'watermelon', 'muskmelon', 'jackfruit'],
                'specialties': 'Cooling vegetables, tropical fruits peak'
            },
            'monsoon': {
                'vegetables': ['turai', 'bhindi', 'karela', 'drumstick'],
                'fruits': ['jamun', 'plums', 'pears'],
                'specialties': 'Limited fresh greens, focus on stored grains'
            }
        }
        
        # Ayurvedic food wisdom by season
        self.ayurvedic_wisdom = {
            'winter': {
                'dosha': 'Vata dominant',
                'food_qualities': 'Warm, moist, heavy, sweet, sour, salty',
                'avoid': 'Cold, dry, light foods',
                'mumbai_adaptation': 'Mild winter allows for lighter warming foods'
            },
            'summer': {
                'dosha': 'Pitta dominant', 
                'food_qualities': 'Cool, liquid, sweet, bitter, astringent',
                'avoid': 'Hot, spicy, oily, salty foods',
                'mumbai_adaptation': 'High humidity needs extra cooling foods'
            },
            'monsoon': {
                'dosha': 'Vata and Kapha imbalance',
                'food_qualities': 'Warm, dry, light, pungent, bitter',
                'avoid': 'Cold, raw, heavy, sweet foods',
                'mumbai_adaptation': 'High humidity weakens digestion'
            }
        }
        
        # Day-specific opening lines (Nigella style)
        self.daily_openings = {
            'Monday': [
                "Mondays, I've always thought, are rather like that first cup of tea in the morning - necessary, but requiring a certain gentle coaxing into existence.",
                "There's something deliciously defiant about cooking something lovely on a Monday, don't you think?",
                "Monday mornings in Mumbai have their own particular brand of optimism, much like the way dal simmers - slowly, then all at once."
            ],
            'Tuesday': [
                "Tuesdays are the middle child of weekdays - overlooked, but often the most interesting when you pay attention.",
                "I find Tuesdays rather like a good curry - they improve as they go along.",
                "There's a quiet confidence to Tuesday cooking, like knowing exactly how much salt to add without measuring."
            ],
            'Wednesday': [
                "Wednesday - that peculiar hump in the week's back, when one needs something both comforting and slightly adventurous.",
                "Midweek meals should be like good friends - reliable, but never boring.",
                "Wednesday cooking is about finding the extraordinary in the perfectly ordinary, rather like Mumbai itself."
            ],
            'Thursday': [
                "Thursday has always struck me as the most hopeful day - close enough to the weekend to dream, far enough to still be practical.",
                "There's something rather thrilling about Thursday evening cooking - the promise of the weekend dancing just out of reach.",
                "Thursday meals should have a certain anticipatory quality, like the pause before the first bite of something divine."
            ],
            'Friday': [
                "Friday! When even the most sensible person allows themselves a small celebration, preferably involving something delicious.",
                "Friday cooking should be joyful, even if it's just the joy of knowing you don't have to think about tomorrow's lunch quite yet.",
                "There's a particular Friday evening energy in Mumbai - part relief, part excitement, entirely edible."
            ],
            'Saturday': [
                "Saturdays are for indulgence, though I've never quite understood why indulgence can't also be nourishing.",
                "Saturday morning cooking has a different rhythm - more languid, like Mumbai's weekend pace.",
                "Weekend cooking should feel like a luxury, even when it's perfectly simple."
            ],
            'Sunday': [
                "Sunday cooking is a meditation, a gentle preparation for the week ahead, seasoned with just a hint of melancholy.",
                "There's something deeply satisfying about Sunday evening meals - they taste of both completion and possibility.",
                "Sunday in Mumbai has its own particular golden light, perfect for slow cooking and slower eating."
            ]
        }
        
        # Seasonal Mumbai commentary
        self.seasonal_commentary = {
            'winter': {
                'general': [
                    "Mumbai's winter is rather like a gentle suggestion - present, but never insistent. Perfect weather for warming spices and comfort food that doesn't overwhelm.",
                    "These pleasant Mumbai evenings call for food that's nourishing without being heavy - rather like wrapping yourself in cashmere instead of wool.",
                    "Winter in Mumbai is deliciously mild, allowing us to enjoy warming foods without the desperate need for them that defines colder climates."
                ],
                'food_philosophy': [
                    "This is the season for gentle heat - not the aggressive spicing of summer, but the warm embrace of ginger, cinnamon, and cardamom.",
                    "Winter vegetables here are particularly sweet - bottle gourds and spinach that taste of sunshine stored up for cooler days.",
                    "Now is the time for slow-cooked dals and gentle khichdis - comfort food that comforts without overwhelming."
                ]
            },
            'summer': {
                'general': [
                    "Mumbai's summer arrives like an overeager dinner guest - earlier than expected and rather more intense than one might prefer.",
                    "The heat here has a particular quality - humid and enveloping, like being wrapped in a warm, damp towel. Not entirely unpleasant, but requiring adjustment.",
                    "Summer in Mumbai teaches patience - with the heat, with the crowds, and with food that must be both cooling and satisfying."
                ],
                'food_philosophy': [
                    "This is the season for foods that cool from within - cucumber, coconut, and the blessed relief of fresh herbs.",
                    "Summer cooking should be like a good friend in crisis - present, helpful, but not demanding too much attention.",
                    "The heat calls for meals that refresh rather than restore - think cooling chutneys and rice that doesn't require much effort to digest."
                ]
            },
            'monsoon': {
                'general': [
                    "Mumbai's monsoon is pure theatre - dramatic, essential, and occasionally inconvenient, rather like a brilliant but temperamental chef.",
                    "The rains here don't just fall, they perform - turning the city into something between Venice and a very large, warm bath.",
                    "Monsoon season brings a particular kind of coziness - the pleasure of being warm and dry while the world outside gets thoroughly soaked."
                ],
                'food_philosophy': [
                    "Monsoon food should match the season's drama - warming spices, hearty dals, and the kind of comfort that comes from a steaming bowl on a grey day.",
                    "This is the season for foods that fight dampness from within - turmeric, ginger, and the gentle heat that keeps the chill at bay.",
                    "Rainy days call for cooking that fills the house with good smells and the heart with contentment - rather like the best kind of hug, but edible."
                ]
            }
        }
        
        # Food philosophy by day
        self.daily_food_philosophy = {
            'Monday': [
                "Monday meals should be gentle but determined - like easing into a warm bath rather than jumping into cold water.",
                "Start the week as you mean to go on - with something that nourishes both body and spirit, preferably without too much fuss.",
                "Monday cooking is about setting intentions - for the week, for your wellbeing, for the small daily pleasures that make everything bearable."
            ],
            'Tuesday': [
                "Tuesday food should have a quiet confidence - nothing showy, but everything exactly as it should be.",
                "Midweek meals are about finding rhythm - the comfortable predictability of good ingredients treated well.",
                "Tuesday cooking is meditation in motion - the kind of gentle focus that makes everything else fall into place."
            ],
            'Wednesday': [
                "Hump day deserves food with a bit of personality - nothing too dramatic, but something that makes you smile.",
                "Wednesday meals should bridge the gap between the week's beginning and its end - substantial enough to sustain, interesting enough to delight.",
                "Midweek cooking is about finding the extraordinary in the everyday - rather like discovering that your daily commute has a beautiful view."
            ],
            'Thursday': [
                "Thursday food should taste of anticipation - the promise of the weekend seasoning everything just a little differently.",
                "Cook something tonight that makes tomorrow feel possible - food as gentle optimism, served warm.",
                "Thursday meals are about building momentum - toward the weekend, toward rest, toward the small celebrations that punctuate our days."
            ],
            'Friday': [
                "Friday cooking should feel celebratory, even if the celebration is simply surviving another week with grace and good humor.",
                "End the working week with something that tastes of satisfaction - not just from eating, but from the simple act of caring for yourself.",
                "Friday food is about transition - from work to rest, from obligation to pleasure, from surviving to thriving."
            ],
            'Saturday': [
                "Saturday meals can afford to be a little more indulgent, a little more time-consuming - weekend cooking as gentle luxury.",
                "Cook something today that you'll remember fondly - not because it's complicated, but because it's made with attention and eaten without hurry.",
                "Weekend cooking is about abundance - not necessarily of ingredients, but of time, attention, and the pleasure of doing things properly."
            ],
            'Sunday': [
                "Sunday cooking is preparation in the deepest sense - for the week ahead, yes, but also for the ongoing project of feeding yourself well.",
                "End the week as you began it - with intention, with care, and with something that tastes of home.",
                "Sunday meals should feel like a gentle conclusion - satisfying enough to complete the week, comforting enough to face the next."
            ]
        }
        
        # Closing thoughts (Nigella style)
        self.closing_thoughts = [
            "Remember, cooking is not about perfection - it's about the gentle act of caring for yourself and those you love, one meal at a time.",
            "The best meals are often the simplest ones, made with attention rather than anxiety, seasoned with contentment rather than stress.",
            "Food, at its heart, is about connection - to the seasons, to tradition, to the simple pleasure of nourishing and being nourished.",
            "Cook with kindness - toward your ingredients, toward yourself, and toward the beautiful imperfection of daily life.",
            "The kitchen is where we practice the small daily magic of transformation - simple ingredients becoming something greater than the sum of their parts.",
            "Good food is a form of love letter - to yourself, to your family, to the idea that life's small pleasures are worth celebrating.",
            "In the end, the best meals are not about what you cook, but about the care with which you cook it - and the joy with which you share it."
        ]
    
    def get_current_season(self) -> str:
        """Determine current Mumbai season"""
        current_month = datetime.now().month
        
        for season, data in self.mumbai_seasons.items():
            if current_month in data['months']:
                return season
        return 'monsoon'  # Default fallback
    
    def get_opening_line(self, day_name: str) -> str:
        """Get Nigella-style opening line for the day"""
        return random.choice(self.daily_openings.get(day_name, self.daily_openings['Monday']))
    
    def get_seasonal_commentary(self) -> str:
        """Get seasonal Mumbai commentary with Hindu/Jain calendar awareness"""
        season = self.get_current_season()
        current_month = datetime.now().month
        
        # Get basic seasonal commentary
        season_data = self.seasonal_commentary[season]
        general = random.choice(season_data['general'])
        philosophy = random.choice(season_data['food_philosophy'])
        
        # Add Hindu calendar context
        hindu_context = self.hindu_calendar.get(current_month, {})
        festivals = hindu_context.get('festivals', [])
        food_wisdom = hindu_context.get('food_wisdom', '')
        ayurvedic_note = hindu_context.get('ayurvedic_note', '')
        
        # Add Jain calendar considerations
        jain_context = ""
        if current_month in [8, 9]:  # Paryushan season
            jain_context = "This is Paryushan season - a time when our Jain friends embrace the most mindful eating, favouring simple, pure foods that honour the principle of ahimsa."
        elif current_month in [6, 7, 8, 9]:  # Chaturmas
            jain_context = "During Chaturmas, the monsoon months, traditional Jain wisdom suggests avoiding green vegetables to minimise harm to growing life - rather wise, given how one's digestion prefers stored grains during the rains anyway."
        
        # Add Mumbai market wisdom
        market_data = self.mumbai_markets[season]
        seasonal_produce = f"The markets are particularly lovely now with {', '.join(market_data['vegetables'][:3])} and {', '.join(market_data['fruits'][:2])}"
        
        # Add Ayurvedic context
        ayurvedic_data = self.ayurvedic_wisdom[season]
        ayurvedic_context = f"Ayurveda suggests this {ayurvedic_data['dosha']} season calls for {ayurvedic_data['food_qualities']} foods - ancient wisdom that makes perfect sense when you consider Mumbai's particular climate."
        
        # Combine all contexts
        enhanced_commentary = f"{general}\n\n{philosophy}"
        
        if festivals:
            enhanced_commentary += f"\n\nWith {', '.join(festivals[:2])} upon us, there's something rather lovely about how our calendar naturally guides us toward {food_wisdom.lower()}."
        
        if jain_context:
            enhanced_commentary += f"\n\n{jain_context}"
        
        enhanced_commentary += f"\n\n{seasonal_produce} - {market_data['specialties'].lower()}. {ayurvedic_context}"
        
        return enhanced_commentary
    
    def get_daily_food_philosophy(self, day_name: str) -> str:
        """Get day-specific food philosophy"""
        return random.choice(self.daily_food_philosophy.get(day_name, self.daily_food_philosophy['Monday']))
    
    def get_closing_thought(self) -> str:
        """Get Nigella-style closing thought"""
        return random.choice(self.closing_thoughts)
    
    def generate_email_intro(self, day_name: str) -> str:
        """Generate complete email introduction"""
        opening = self.get_opening_line(day_name)
        seasonal = self.get_seasonal_commentary()
        philosophy = self.get_daily_food_philosophy(day_name)
        
        return f"""Darlings,

{opening}

{seasonal}

{philosophy}

Now, about today's menu..."""
    
    def generate_email_closing(self, day_name: str) -> str:
        """Generate complete email closing"""
        closing_thought = self.get_closing_thought()
        
        # Season-specific sign-off
        season = self.get_current_season()
        season_name = self.mumbai_seasons[season]['name']
        
        return f"""

{closing_thought}

Cook with love, eat with joy, and remember that even the simplest meal becomes special when made with care.

With warmth from Mumbai's {season_name.lower()},

Nigela 🤍

P.S. Do screenshot the menu table above - it's perfectly sized for sharing with your cook, and there's something rather satisfying about having the whole day's plan captured in one elegant frame."""

# Test the persona
if __name__ == "__main__":
    persona = NigellaPersona()
    
    today = datetime.now().strftime('%A')
    
    print("🎭 NIGELLA LAWSON PERSONA TEST")
    print("=" * 50)
    
    print("📧 EMAIL INTRODUCTION:")
    print(persona.generate_email_intro(today))
    
    print("\n" + "=" * 50)
    
    print("📧 EMAIL CLOSING:")
    print(persona.generate_email_closing(today))
    
    print("\n✅ Nigella persona ready for integration!")
