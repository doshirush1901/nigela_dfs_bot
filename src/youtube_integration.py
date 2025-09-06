"""
YouTube Video Integration for Nigela
Finds relevant cooking videos for recipes using YouTube Data API and web scraping
"""

import asyncio
import re
from typing import List, Dict, Optional
import httpx
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

class YouTubeVideoFinder:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_search_url = "https://www.youtube.com/results?search_query="
        
    async def search_videos_web(self, recipe_name: str, cuisine_hint: str = None) -> List[Dict[str, str]]:
        """Search YouTube videos using web scraping (no API key needed)"""
        
        # Build search query
        search_terms = []
        search_terms.append(recipe_name)
        if cuisine_hint:
            search_terms.append(cuisine_hint)
        search_terms.extend(["recipe", "cooking", "how to make"])
        
        query = " ".join(search_terms)
        search_url = self.base_search_url + quote_plus(query)
        
        videos = []
        
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = await client.get(search_url, headers=headers)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract video data from YouTube search results
                script_tags = soup.find_all('script')
                
                for script in script_tags:
                    if script.string and 'var ytInitialData' in script.string:
                        # Parse YouTube's initial data
                        script_content = script.string
                        
                        # Extract video IDs and titles using regex
                        video_pattern = r'"videoId":"([^"]+)".*?"title":{"runs":\[{"text":"([^"]+)"}\]'
                        matches = re.findall(video_pattern, script_content)
                        
                        for video_id, title in matches[:5]:  # Get first 5 videos
                            # Filter for cooking-related videos
                            if any(keyword in title.lower() for keyword in ['recipe', 'cooking', 'how to', 'make', recipe_name.lower()]):
                                videos.append({
                                    'title': title,
                                    'url': f'https://www.youtube.com/watch?v={video_id}',
                                    'video_id': video_id,
                                    'thumbnail': f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
                                })
                        break
                        
        except Exception as e:
            print(f"⚠️ YouTube search error for '{recipe_name}': {e}")
            
        return videos[:3]  # Return top 3 videos
    
    async def search_videos_api(self, recipe_name: str, cuisine_hint: str = None) -> List[Dict[str, str]]:
        """Search YouTube videos using official API (requires API key)"""
        
        if not self.api_key:
            return await self.search_videos_web(recipe_name, cuisine_hint)
            
        # Build search query
        query_parts = [recipe_name, "recipe", "cooking"]
        if cuisine_hint:
            query_parts.append(cuisine_hint)
        query = " ".join(query_parts)
        
        api_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': 5,
            'key': self.api_key,
            'regionCode': 'IN',  # Focus on Indian content
            'relevanceLanguage': 'en'
        }
        
        videos = []
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(api_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                for item in data.get('items', []):
                    snippet = item['snippet']
                    video_id = item['id']['videoId']
                    
                    videos.append({
                        'title': snippet['title'],
                        'url': f'https://www.youtube.com/watch?v={video_id}',
                        'video_id': video_id,
                        'thumbnail': snippet['thumbnails']['medium']['url'],
                        'channel': snippet['channelTitle'],
                        'description': snippet['description'][:200] + '...'
                    })
                    
        except Exception as e:
            print(f"⚠️ YouTube API error for '{recipe_name}': {e}")
            # Fallback to web scraping
            return await self.search_videos_web(recipe_name, cuisine_hint)
            
        return videos[:3]
    
    def get_best_video_for_recipe(self, recipe_name: str, cuisine_hint: str = None) -> Optional[Dict[str, str]]:
        """Get the best video for a recipe (synchronous wrapper)"""
        try:
            videos = asyncio.run(self.search_videos_web(recipe_name, cuisine_hint))
            return videos[0] if videos else None
        except Exception:
            return None

# Enhanced recipe class with video support
def enhance_dish_with_video(dish, youtube_finder: YouTubeVideoFinder = None) -> None:
    """Add YouTube video link to a dish object"""
    if not youtube_finder:
        youtube_finder = YouTubeVideoFinder()
    
    try:
        # Determine cuisine hint from tags
        cuisine_hint = None
        for tag in getattr(dish, 'tags', []):
            if 'cuisine:' in tag:
                cuisine_hint = tag.replace('cuisine:', '')
                break
        
        # Get video for this recipe
        video = youtube_finder.get_best_video_for_recipe(dish.name, cuisine_hint)
        
        if video:
            # Add video attributes to dish
            dish.video_url = video['url']
            dish.video_title = video['title']
            dish.video_thumbnail = video.get('thumbnail')
            print(f"🎥 Found video for {dish.name}: {video['title'][:50]}...")
        else:
            dish.video_url = None
            dish.video_title = None
            dish.video_thumbnail = None
            
    except Exception as e:
        print(f"⚠️ Video search failed for {dish.name}: {e}")
        dish.video_url = None
        dish.video_title = None
        dish.video_thumbnail = None

# Batch video enhancement
async def enhance_recipes_with_videos(dishes: List, max_concurrent: int = 3):
    """Add YouTube videos to multiple recipes efficiently"""
    youtube_finder = YouTubeVideoFinder()
    
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def enhance_single_dish(dish):
        async with semaphore:
            # Determine cuisine hint
            cuisine_hint = None
            for tag in getattr(dish, 'tags', []):
                if 'cuisine:' in tag:
                    cuisine_hint = tag.replace('cuisine:', '')
                    break
            
            # Search for videos
            videos = await youtube_finder.search_videos_web(dish.name, cuisine_hint)
            
            if videos:
                video = videos[0]  # Take best match
                dish.video_url = video['url']
                dish.video_title = video['title']
                dish.video_thumbnail = video.get('thumbnail')
                print(f"🎥 {dish.name} → {video['title'][:40]}...")
            else:
                dish.video_url = None
                print(f"❌ No video found for {dish.name}")
    
    # Process all dishes concurrently
    await asyncio.gather(*[enhance_single_dish(dish) for dish in dishes])
    
    return dishes

if __name__ == "__main__":
    # Test the YouTube integration
    finder = YouTubeVideoFinder()
    
    test_recipes = ["Ragi Dosa", "Gujarati Dal", "Paneer Makhni", "Masala Chai"]
    
    for recipe in test_recipes:
        video = finder.get_best_video_for_recipe(recipe, "indian")
        if video:
            print(f"✅ {recipe}: {video['title']}")
            print(f"   🔗 {video['url']}")
        else:
            print(f"❌ {recipe}: No video found")
        print()
