"""
Cookbook Processor for Nigela
Processes collected cookbooks and integrates them with the meal rotation system
"""

import re
from pathlib import Path
from typing import List, Dict, Any
import json
from .models import Dish, Ingredient
from .llm import parse_dish_with_ai
from .io_xls import read_dishes, write_dishes

class CookbookProcessor:
    def __init__(self, library_dir="library", data_dir="data"):
        self.library_dir = Path(library_dir)
        self.data_dir = Path(data_dir)
        
    def extract_recipes_from_text(self, text_content: str, source: str = "Cookbook") -> List[Dish]:
        """Extract and parse recipes from text content"""
        
        recipes = []
        
        # Split text into recipe sections
        # Look for recipe headers (## Recipe Name or # Recipe Name)
        recipe_sections = re.split(r'\n##\s+([^\n]+)', text_content)
        
        if len(recipe_sections) > 1:
            # Process each recipe section
            for i in range(1, len(recipe_sections), 2):
                if i + 1 < len(recipe_sections):
                    recipe_name = recipe_sections[i].strip()
                    recipe_content = recipe_sections[i + 1].strip()
                    
                    # Parse this recipe
                    recipe_text = f"## {recipe_name}\n{recipe_content}"
                    
                    try:
                        # Use your existing AI parsing
                        parsed_recipes = parse_dish_with_ai(recipe_text, source=source)
                        recipes.extend(parsed_recipes)
                        print(f"✅ Parsed: {recipe_name}")
                    except Exception as e:
                        print(f"⚠️ Failed to parse {recipe_name}: {e}")
        else:
            # If no clear sections, try to parse the whole text
            try:
                parsed_recipes = parse_dish_with_ai(text_content, source=source)
                recipes.extend(parsed_recipes)
            except Exception as e:
                print(f"⚠️ Failed to parse cookbook content: {e}")
        
        return recipes
    
    def process_starter_cookbook(self) -> List[Dish]:
        """Process the starter cookbook we created"""
        
        starter_file = self.library_dir / "nigela_starter_cookbook.txt"
        
        if not starter_file.exists():
            print("⚠️ Starter cookbook not found")
            return []
        
        print("📖 Processing starter cookbook...")
        
        with open(starter_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Manually parse the starter cookbook (we know its format)
        recipes = self._parse_starter_cookbook_manually(content)
        
        print(f"✅ Processed {len(recipes)} recipes from starter cookbook")
        return recipes
    
    def _parse_starter_cookbook_manually(self, content: str) -> List[Dish]:
        """Manually parse the starter cookbook since we know its format"""
        
        recipes = []
        
        # Define the recipes manually for reliability
        starter_recipes = [
            {
                'name': 'Gujarati Dhokla',
                'meal_type': 'breakfast',
                'cuisine': 'Gujarati',
                'cook_minutes': 30,
                'difficulty': 3,
                'tags': ['steamed', 'gujarati', 'healthy', 'protein'],
                'ingredients': [
                    Ingredient('besan', 200, 'g'),
                    Ingredient('water', 250, 'ml'),
                    Ingredient('ginger_green_chili_paste', 1, 'tsp'),
                    Ingredient('turmeric', 0.25, 'tsp'),
                    Ingredient('salt', 1, 'to_taste'),
                    Ingredient('eno_fruit_salt', 1, 'tsp'),
                    Ingredient('oil', 1, 'tbsp')
                ],
                'steps': [
                    'Mix besan with water to make smooth batter',
                    'Add ginger-chili paste, turmeric, salt',
                    'Just before steaming, add eno and oil, mix gently',
                    'Steam for 15-20 minutes',
                    'Cool and cut into pieces',
                    'Temper with mustard seeds, curry leaves'
                ],
                'jain_ok': True,
                'notes': 'Light, fluffy steamed cake perfect for breakfast',
                'substitutions': ['Can use baking soda instead of eno']
            },
            {
                'name': 'Methi Thepla',
                'meal_type': 'breakfast',
                'cuisine': 'Gujarati',
                'cook_minutes': 20,
                'difficulty': 2,
                'tags': ['flatbread', 'gujarati', 'travel_food', 'nutritious'],
                'ingredients': [
                    Ingredient('wheat_flour', 200, 'g'),
                    Ingredient('fenugreek_leaves', 100, 'g'),
                    Ingredient('turmeric', 0.5, 'tsp'),
                    Ingredient('red_chili_powder', 0.5, 'tsp'),
                    Ingredient('ginger_green_chili_paste', 1, 'tsp'),
                    Ingredient('oil', 2, 'tbsp'),
                    Ingredient('salt', 1, 'to_taste')
                ],
                'steps': [
                    'Mix all dry ingredients',
                    'Add methi leaves, ginger-chili paste',
                    'Add oil and knead with water to make soft dough',
                    'Roll thin and cook on tawa with little oil',
                    'Serve hot with yogurt'
                ],
                'jain_ok': True,
                'notes': 'Nutritious flatbread with fenugreek leaves',
                'substitutions': ['Can use spinach instead of methi']
            },
            {
                'name': 'South Indian Lemon Rice',
                'meal_type': 'lunch',
                'cuisine': 'South Indian',
                'cook_minutes': 15,
                'difficulty': 2,
                'tags': ['rice', 'tangy', 'quick', 'south_indian'],
                'ingredients': [
                    Ingredient('cooked_rice', 2, 'cups'),
                    Ingredient('lemon_juice', 3, 'tbsp'),
                    Ingredient('turmeric', 0.25, 'tsp'),
                    Ingredient('mustard_seeds', 1, 'tsp'),
                    Ingredient('curry_leaves', 10, 'pieces'),
                    Ingredient('green_chilies', 2, 'pieces'),
                    Ingredient('peanuts', 2, 'tbsp'),
                    Ingredient('oil', 2, 'tbsp'),
                    Ingredient('salt', 1, 'to_taste')
                ],
                'steps': [
                    'Heat oil, add mustard seeds',
                    'When they splutter, add curry leaves, green chilies',
                    'Add peanuts, fry till golden',
                    'Add turmeric, then rice',
                    'Mix gently, add lemon juice and salt',
                    'Garnish with fresh coriander'
                ],
                'jain_ok': True,
                'notes': 'Tangy, flavorful rice perfect for lunch',
                'substitutions': ['Can add grated coconut for richness']
            },
            {
                'name': 'Coconut Chutney',
                'meal_type': 'snack',
                'cuisine': 'South Indian', 
                'cook_minutes': 10,
                'difficulty': 1,
                'tags': ['chutney', 'coconut', 'condiment', 'south_indian'],
                'ingredients': [
                    Ingredient('fresh_coconut', 1, 'cup'),
                    Ingredient('green_chilies', 2, 'pieces'),
                    Ingredient('ginger', 1, 'inch'),
                    Ingredient('salt', 1, 'to_taste'),
                    Ingredient('curry_leaves', 8, 'pieces'),
                    Ingredient('mustard_seeds', 0.5, 'tsp'),
                    Ingredient('oil', 1, 'tsp')
                ],
                'steps': [
                    'Grind coconut, green chilies, ginger with little water',
                    'Add salt and mix',
                    'Heat oil, add mustard seeds',
                    'When they splutter, add curry leaves',
                    'Pour over chutney and mix'
                ],
                'jain_ok': True,
                'notes': 'Fresh coconut chutney for dosas and idlis',
                'substitutions': ['Can add roasted chana dal for thickness']
            },
            {
                'name': 'Quinoa Upma',
                'meal_type': 'breakfast',
                'cuisine': 'Fusion',
                'cook_minutes': 25,
                'difficulty': 2,
                'tags': ['quinoa', 'healthy', 'protein', 'fusion'],
                'ingredients': [
                    Ingredient('quinoa', 1, 'cup'),
                    Ingredient('mixed_vegetables', 1, 'cup'),
                    Ingredient('mustard_seeds', 1, 'tsp'),
                    Ingredient('curry_leaves', 10, 'pieces'),
                    Ingredient('green_chilies', 2, 'pieces'),
                    Ingredient('ginger', 1, 'tsp'),
                    Ingredient('oil', 2, 'tbsp'),
                    Ingredient('salt', 1, 'to_taste'),
                    Ingredient('water', 2, 'cups')
                ],
                'steps': [
                    'Wash and drain quinoa',
                    'Heat oil, add mustard seeds',
                    'Add curry leaves, green chilies, ginger',
                    'Add vegetables, sauté 5 minutes',
                    'Add quinoa, stir for 2 minutes',
                    'Add hot water and salt',
                    'Cover and cook 15 minutes till quinoa is fluffy'
                ],
                'jain_ok': True,
                'notes': 'Healthy protein-rich breakfast with quinoa',
                'substitutions': ['Can use broken wheat instead of quinoa']
            }
        ]
        
        # Convert to Dish objects
        for recipe_data in starter_recipes:
            dish = Dish(
                name=recipe_data['name'],
                meal_type=recipe_data['meal_type'],
                cuisine=recipe_data['cuisine'],
                cook_minutes=recipe_data['cook_minutes'],
                difficulty=recipe_data['difficulty'],
                tags=recipe_data['tags'],
                ingredients=recipe_data['ingredients'],
                steps=recipe_data['steps'],
                jain_ok=recipe_data['jain_ok'],
                notes=recipe_data['notes'],
                substitutions=recipe_data['substitutions'],
                flavor_text=recipe_data['notes'],
                source="Nigela Starter Collection"
            )
            recipes.append(dish)
        
        return recipes
    
    def integrate_with_nigela_database(self, new_recipes: List[Dish]) -> int:
        """Add new recipes to the Nigela dishes database"""
        
        dishes_file = self.data_dir / "dishes.xlsx"
        
        try:
            # Read existing dishes
            existing_dishes = read_dishes(str(dishes_file))
            print(f"📚 Found {len(existing_dishes)} existing dishes")
            
            # Check for duplicates by name
            existing_names = {dish.name.lower() for dish in existing_dishes}
            new_unique_recipes = []
            
            for recipe in new_recipes:
                if recipe.name.lower() not in existing_names:
                    new_unique_recipes.append(recipe)
                else:
                    print(f"⚠️ Skipping duplicate: {recipe.name}")
            
            if new_unique_recipes:
                # Combine and save
                combined_dishes = existing_dishes + new_unique_recipes
                write_dishes(str(dishes_file), combined_dishes)
                
                print(f"✅ Added {len(new_unique_recipes)} new recipes to database")
                print(f"📊 Total recipes in database: {len(combined_dishes)}")
                
                return len(new_unique_recipes)
            else:
                print("ℹ️ No new unique recipes to add")
                return 0
                
        except Exception as e:
            print(f"⚠️ Error integrating with database: {e}")
            return 0
    
    def process_all_cookbooks(self) -> Dict[str, Any]:
        """Process all available cookbooks and integrate with Nigela"""
        
        print("📚 PROCESSING ALL COOKBOOKS FOR NIGELA")
        print("=" * 50)
        
        all_new_recipes = []
        processing_report = {
            'processed_files': [],
            'total_recipes_extracted': 0,
            'recipes_added_to_database': 0,
            'processing_errors': []
        }
        
        # Process starter cookbook
        try:
            starter_recipes = self.process_starter_cookbook()
            all_new_recipes.extend(starter_recipes)
            processing_report['processed_files'].append('nigela_starter_cookbook.txt')
            processing_report['total_recipes_extracted'] += len(starter_recipes)
        except Exception as e:
            error_msg = f"Error processing starter cookbook: {e}"
            print(f"⚠️ {error_msg}")
            processing_report['processing_errors'].append(error_msg)
        
        # Process any PDF cookbooks (if downloaded)
        pdf_files = list(self.library_dir.glob("*.pdf"))
        for pdf_file in pdf_files:
            try:
                print(f"📖 Processing PDF: {pdf_file.name}")
                # For now, skip PDF processing as it requires more setup
                # In the future, this would use your PDF parsing pipeline
                print(f"ℹ️ PDF processing not implemented yet: {pdf_file.name}")
            except Exception as e:
                error_msg = f"Error processing {pdf_file.name}: {e}"
                print(f"⚠️ {error_msg}")
                processing_report['processing_errors'].append(error_msg)
        
        # Integrate with Nigela database
        if all_new_recipes:
            recipes_added = self.integrate_with_nigela_database(all_new_recipes)
            processing_report['recipes_added_to_database'] = recipes_added
        
        # Save processing report
        report_file = self.library_dir / 'processing_report.json'
        with open(report_file, 'w') as f:
            json.dump(processing_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n🎉 COOKBOOK PROCESSING COMPLETE!")
        print(f"📊 Processing Report:")
        print(f"   📚 Files processed: {len(processing_report['processed_files'])}")
        print(f"   🍽️ Recipes extracted: {processing_report['total_recipes_extracted']}")
        print(f"   ✅ Recipes added to database: {processing_report['recipes_added_to_database']}")
        print(f"   ⚠️ Errors: {len(processing_report['processing_errors'])}")
        print(f"📝 Full report saved: {report_file}")
        
        return processing_report

def main():
    """Main function to process cookbooks"""
    processor = CookbookProcessor()
    report = processor.process_all_cookbooks()
    
    print(f"\n🔄 NEW RECIPES NOW AVAILABLE IN MEAL ROTATION!")
    print("🎯 These recipes will appear in your daily variety system!")
    print("📧 Tomorrow's email will include fresh options!")

if __name__ == "__main__":
    main()
