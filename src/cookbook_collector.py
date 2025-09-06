"""
Cookbook Collector for Nigela - Multiple Sources
Since LibGen has access issues, we'll use multiple reliable sources
"""

import requests
import asyncio
import httpx
from pathlib import Path
from typing import List, Dict
import json
import time
from urllib.parse import quote_plus

class CookbookCollector:
    def __init__(self, data_dir="library"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Your taste profile for targeted collection
        self.taste_keywords = [
            "indian vegetarian recipes",
            "gujarati cookbook",
            "south indian vegetarian",
            "jain recipes cookbook",
            "healthy indian cooking",
            "ayurvedic recipes",
            "tarla dalal recipes",
            "sanjeev kapoor vegetarian",
            "plant based indian",
            "traditional indian vegetarian"
        ]
        
        # Multiple sources for cookbook collection
        self.sources = {
            'archive_org': 'https://archive.org/search.php',
            'gutenberg': 'https://www.gutenberg.org/ebooks/search/',
            'openlibrary': 'https://openlibrary.org/search.json'
        }
    
    def search_archive_org_cookbooks(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search Archive.org for cookbooks - they have many public domain cookbooks"""
        
        print(f"🔍 Searching Archive.org for: {query}")
        results = []
        
        try:
            search_url = "https://archive.org/advancedsearch.php"
            params = {
                'q': f'title:({query}) AND mediatype:texts AND subject:cooking',
                'fl': 'identifier,title,creator,date,downloads,format',
                'sort[]': 'downloads desc',
                'rows': max_results,
                'page': 1,
                'output': 'json'
            }
            
            response = requests.get(search_url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            for item in data.get('response', {}).get('docs', []):
                # Check if it has PDF format
                formats = item.get('format', [])
                if isinstance(formats, str):
                    formats = [formats]
                
                has_pdf = any('PDF' in fmt.upper() for fmt in formats)
                
                if has_pdf:
                    cookbook = {
                        'title': item.get('title', 'Unknown Title'),
                        'author': item.get('creator', ['Unknown Author'])[0] if item.get('creator') else 'Unknown Author',
                        'year': item.get('date', 'Unknown'),
                        'identifier': item.get('identifier', ''),
                        'downloads': item.get('downloads', 0),
                        'source': 'Archive.org',
                        'download_url': f"https://archive.org/download/{item.get('identifier')}/{item.get('identifier')}.pdf",
                        'formats': formats
                    }
                    
                    if self._is_relevant_cookbook_archive(cookbook):
                        results.append(cookbook)
                        print(f"📚 Found: {cookbook['title']} by {cookbook['author']}")
        
        except Exception as e:
            print(f"⚠️ Error searching Archive.org: {e}")
        
        return results
    
    def _is_relevant_cookbook_archive(self, cookbook: Dict) -> bool:
        """Check if Archive.org cookbook matches your taste profile"""
        
        title_lower = cookbook['title'].lower()
        author_lower = cookbook['author'].lower()
        
        # Must be cookbook-related
        cookbook_indicators = ['cookbook', 'recipe', 'cooking', 'kitchen', 'food', 'cuisine']
        if not any(indicator in title_lower for indicator in cookbook_indicators):
            return False
        
        # Relevance scoring
        score = 0
        
        # Indian cuisine
        if any(word in title_lower for word in ['indian', 'gujarati', 'bengali', 'south indian']):
            score += 5
        
        # Vegetarian
        if any(word in title_lower for word in ['vegetarian', 'vegan', 'plant']):
            score += 3
        
        # Healthy/traditional
        if any(word in title_lower for word in ['healthy', 'traditional', 'home']):
            score += 2
        
        # Popular downloads (indicates quality)
        if cookbook.get('downloads', 0) > 100:
            score += 1
        
        return score >= 2
    
    async def download_cookbook_async(self, cookbook: Dict) -> Path:
        """Download cookbook asynchronously"""
        
        # Create safe filename
        safe_title = "".join(c for c in cookbook['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:50]
        filename = f"{safe_title}_{cookbook.get('year', 'unknown')}.pdf"
        filepath = self.data_dir / filename
        
        if filepath.exists():
            print(f"📚 Already have: {filename}")
            return filepath
        
        try:
            print(f"⬇️ Downloading: {cookbook['title']}")
            
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(cookbook['download_url'])
                response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"✅ Downloaded: {filename}")
                return filepath
                
        except Exception as e:
            print(f"⚠️ Download failed for {cookbook['title']}: {e}")
            return None
    
    def search_free_cookbook_websites(self) -> List[Dict]:
        """Search for free cookbook websites and resources"""
        
        free_cookbooks = [
            {
                'title': 'The Vegetarian Cookbook - Indian Recipes',
                'author': 'Various Traditional Sources',
                'year': '2020',
                'source': 'Community Collection',
                'download_url': 'https://example.com/vegetarian-indian.pdf',  # Placeholder
                'description': 'Traditional Indian vegetarian recipes'
            }
        ]
        
        # Add known free cookbook resources
        known_sources = [
            "Project Gutenberg cookbooks",
            "Wikibooks cookbook collection", 
            "Open Library cookbooks",
            "Government nutrition guides"
        ]
        
        print("📚 Known free cookbook sources:")
        for source in known_sources:
            print(f"   • {source}")
        
        return free_cookbooks
    
    async def collect_cookbooks_for_nigela(self, max_downloads: int = 10) -> List[Path]:
        """Main collection function"""
        
        print("📚 COLLECTING COOKBOOKS FOR NIGELA")
        print("=" * 50)
        
        all_cookbooks = []
        
        # Search Archive.org for each keyword
        for keyword in self.taste_keywords[:5]:  # Limit to avoid rate limiting
            try:
                cookbooks = self.search_archive_org_cookbooks(keyword, max_results=5)
                all_cookbooks.extend(cookbooks)
                await asyncio.sleep(1)  # Be respectful
            except Exception as e:
                print(f"⚠️ Search failed for '{keyword}': {e}")
        
        # Remove duplicates
        unique_cookbooks = {}
        for cookbook in all_cookbooks:
            key = cookbook['identifier'] if 'identifier' in cookbook else cookbook['title'].lower()
            if key not in unique_cookbooks:
                unique_cookbooks[key] = cookbook
        
        print(f"📚 Found {len(unique_cookbooks)} unique cookbooks")
        
        # Sort by relevance and downloads
        sorted_cookbooks = sorted(
            unique_cookbooks.values(),
            key=lambda x: (x.get('downloads', 0), self._calculate_relevance(x)),
            reverse=True
        )
        
        # Download top cookbooks
        downloaded_files = []
        semaphore = asyncio.Semaphore(2)  # Max 2 concurrent downloads
        
        async def download_with_semaphore(cookbook):
            async with semaphore:
                return await self.download_cookbook_async(cookbook)
        
        tasks = [download_with_semaphore(cb) for cb in sorted_cookbooks[:max_downloads]]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        downloaded_files = [f for f in results if isinstance(f, Path) and f.exists()]
        
        print(f"✅ Successfully downloaded {len(downloaded_files)} cookbooks!")
        
        # Save collection report
        self._save_collection_report(sorted_cookbooks, downloaded_files)
        
        return downloaded_files
    
    def _calculate_relevance(self, cookbook: Dict) -> int:
        """Calculate cookbook relevance score"""
        score = 0
        title_lower = cookbook['title'].lower()
        
        # Indian cuisine bonus
        if any(word in title_lower for word in ['indian', 'gujarati', 'bengali']):
            score += 10
        
        # Vegetarian bonus  
        if any(word in title_lower for word in ['vegetarian', 'vegan']):
            score += 8
        
        # Healthy cooking bonus
        if any(word in title_lower for word in ['healthy', 'ayurvedic']):
            score += 5
        
        return score
    
    def _save_collection_report(self, all_cookbooks: List[Dict], downloaded_files: List[Path]):
        """Save collection report"""
        
        report = {
            'collection_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_cookbooks_found': len(all_cookbooks),
            'cookbooks_downloaded': len(downloaded_files),
            'downloaded_files': [str(f) for f in downloaded_files],
            'top_cookbooks': all_cookbooks[:20]
        }
        
        report_file = self.data_dir / 'cookbook_collection_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Collection report saved: {report_file}")

# Create a simple manual cookbook list for immediate use
def create_starter_cookbook_collection():
    """Create a starter collection of known good cookbooks"""
    
    starter_cookbooks = [
        {
            'title': 'Traditional Indian Vegetarian Recipes',
            'content': '''
# GUJARATI CLASSICS

## Dhokla (Steamed Chickpea Cake)
**Cook Time**: 30 minutes
**Ingredients**: 
- Besan (chickpea flour) 200g
- Water 250ml  
- Ginger-green chili paste 1 tsp
- Turmeric 1/4 tsp
- Salt to taste
- Eno fruit salt 1 tsp
- Oil 1 tbsp

**Method**:
1. Mix besan with water to make smooth batter
2. Add ginger-chili paste, turmeric, salt
3. Just before steaming, add eno and oil, mix gently
4. Steam for 15-20 minutes
5. Cool and cut into pieces
6. Temper with mustard seeds, curry leaves

## Thepla (Spiced Flatbread)
**Cook Time**: 20 minutes
**Ingredients**:
- Wheat flour 200g
- Fenugreek leaves (methi) 100g chopped
- Turmeric 1/2 tsp
- Red chili powder 1/2 tsp
- Ginger-green chili paste 1 tsp
- Oil 2 tbsp
- Salt to taste

**Method**:
1. Mix all dry ingredients
2. Add methi leaves, ginger-chili paste
3. Add oil and knead with water to make soft dough
4. Roll thin and cook on tawa with little oil
5. Serve hot with yogurt

# SOUTH INDIAN FAVORITES

## Lemon Rice
**Cook Time**: 15 minutes  
**Ingredients**:
- Cooked rice 2 cups
- Lemon juice 3 tbsp
- Turmeric 1/4 tsp
- Mustard seeds 1 tsp
- Curry leaves 8-10
- Green chilies 2 slit
- Peanuts 2 tbsp
- Oil 2 tbsp
- Salt to taste

**Method**:
1. Heat oil, add mustard seeds
2. When they splutter, add curry leaves, green chilies
3. Add peanuts, fry till golden
4. Add turmeric, then rice
5. Mix gently, add lemon juice and salt
6. Garnish with fresh coriander

## Coconut Chutney
**Cook Time**: 10 minutes
**Ingredients**:
- Fresh coconut 1 cup grated
- Green chilies 2
- Ginger 1 inch piece
- Salt to taste
- Curry leaves 6-8
- Mustard seeds 1/2 tsp
- Oil 1 tsp

**Method**:
1. Grind coconut, green chilies, ginger with little water
2. Add salt and mix
3. Heat oil, add mustard seeds
4. When they splutter, add curry leaves
5. Pour over chutney and mix

# HEALTHY BOWLS

## Quinoa Upma
**Cook Time**: 25 minutes
**Ingredients**:
- Quinoa 1 cup
- Mixed vegetables 1 cup diced
- Mustard seeds 1 tsp
- Curry leaves 8-10
- Green chilies 2 slit
- Ginger 1 tsp minced
- Oil 2 tbsp
- Salt to taste
- Water 2 cups

**Method**:
1. Wash and drain quinoa
2. Heat oil, add mustard seeds
3. Add curry leaves, green chilies, ginger
4. Add vegetables, sauté 5 minutes
5. Add quinoa, stir for 2 minutes
6. Add hot water and salt
7. Cover and cook 15 minutes till quinoa is fluffy
            ''',
            'source': 'Nigela Starter Collection'
        }
    ]
    
    # Save starter collection
    library_dir = Path("library")
    library_dir.mkdir(exist_ok=True)
    
    starter_file = library_dir / "nigela_starter_cookbook.txt"
    with open(starter_file, 'w', encoding='utf-8') as f:
        f.write(starter_cookbooks[0]['content'])
    
    print("📚 Created starter cookbook collection!")
    print(f"📝 Saved to: {starter_file}")
    
    return [starter_file]

async def main():
    """Main collection function"""
    
    print("🍽️ NIGELA COOKBOOK COLLECTION SYSTEM")
    print("=" * 50)
    
    # First, create starter collection
    starter_files = create_starter_cookbook_collection()
    
    # Then try to collect from Archive.org
    collector = CookbookCollector()
    try:
        downloaded_files = await collector.collect_cookbooks_for_nigela(max_downloads=5)
        all_files = starter_files + downloaded_files
    except Exception as e:
        print(f"⚠️ Collection error: {e}")
        all_files = starter_files
    
    print(f"\n📚 COLLECTION COMPLETE!")
    print(f"✅ Total cookbooks available: {len(all_files)}")
    
    for file in all_files:
        print(f"   📖 {file.name}")
    
    print(f"\n🔗 Ready to integrate with Nigela recipe system!")
    print("Next: Process these cookbooks to extract recipes for your daily variety system!")
    
    return all_files

if __name__ == "__main__":
    asyncio.run(main())
