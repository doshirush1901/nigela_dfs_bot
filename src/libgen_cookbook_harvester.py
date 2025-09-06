"""
Library Genesis Cookbook Harvester for Nigela
Targets cookbooks matching your taste profile: Indian vegetarian, healthy, Jain-friendly
"""

import requests
import time
import re
import json
from pathlib import Path
from typing import List, Dict, Optional
import urllib.parse
from bs4 import BeautifulSoup
import asyncio
import httpx

class LibgenCookbookHarvester:
    def __init__(self, data_dir="library"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Your taste profile keywords for targeted search
        self.taste_profile_keywords = [
            # Indian vegetarian
            "indian vegetarian cookbook",
            "gujarati recipes",
            "south indian vegetarian",
            "north indian vegetarian",
            "maharashtrian recipes",
            "bengali vegetarian",
            "punjabi vegetarian",
            "rajasthani recipes",
            
            # Healthy & wellness
            "healthy indian cooking",
            "ayurvedic recipes",
            "satvik cooking",
            "plant based indian",
            "vegan indian recipes",
            "diabetes friendly indian",
            "weight loss indian recipes",
            
            # Jain & special diets
            "jain recipes",
            "jain cookbook",
            "no onion no garlic",
            "pure vegetarian",
            "swaminarayan recipes",
            
            # Modern healthy
            "quinoa indian recipes",
            "millet recipes india",
            "gluten free indian",
            "keto indian recipes",
            "superfood indian cooking",
            
            # Traditional & authentic
            "traditional indian recipes",
            "authentic indian vegetarian",
            "home style indian cooking",
            "regional indian cuisine",
            "festival recipes india",
            
            # Specific authors/chefs
            "tarla dalal",
            "sanjeev kapoor vegetarian",
            "madhur jaffrey vegetarian",
            "julie sahni",
            "yamuna devi"
        ]
        
        self.libgen_mirrors = [
            "https://libgen.li/",
            "https://libgen.vg/",
            "https://libgen.la/"
        ]
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
    def search_cookbooks(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search Library Genesis for cookbooks matching query"""
        
        results = []
        
        for mirror in self.libgen_mirrors:
            try:
                print(f"🔍 Searching {mirror} for: {query}")
                
                # Correct LibGen search URL format
                search_url = f"{mirror}index.php"
                params = {
                    'req': query,
                    'columns[]': ['t', 'a', 's', 'y', 'p'],  # title, author, series, year, pages
                    'topics[]': 'l',  # libgen topic
                    'res': max_results,
                    'gmode': 'on'  # Google mode for better search
                }
                
                response = self.session.get(search_url, params=params, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Parse search results
                for row in soup.find_all('tr')[1:]:  # Skip header
                    cells = row.find_all('td')
                    if len(cells) >= 10:
                        
                        # Extract book info
                        title_cell = cells[2]
                        title_link = title_cell.find('a')
                        title = title_link.text.strip() if title_link else cells[2].get_text(strip=True)
                        
                        author = cells[1].get_text(strip=True)
                        year = cells[4].get_text(strip=True)
                        pages = cells[5].get_text(strip=True)
                        language = cells[6].get_text(strip=True)
                        size = cells[7].get_text(strip=True)
                        extension = cells[8].get_text(strip=True)
                        
                        # Get download links
                        download_links = []
                        for link in cells[9].find_all('a'):
                            if link.get('href'):
                                download_links.append(mirror + link['href'])
                        
                        book_info = {
                            'title': title,
                            'author': author,
                            'year': year,
                            'pages': pages,
                            'language': language,
                            'size': size,
                            'extension': extension,
                            'download_links': download_links,
                            'query': query,
                            'source_mirror': mirror
                        }
                        
                        # Filter for relevant cookbooks
                        if self._is_relevant_cookbook(book_info):
                            results.append(book_info)
                            print(f"📚 Found: {title} by {author} ({year})")
                
                if results:
                    break  # Found results, no need to try other mirrors
                    
            except Exception as e:
                print(f"⚠️ Error searching {mirror}: {e}")
                continue
        
        return results
    
    def _is_relevant_cookbook(self, book_info: Dict) -> bool:
        """Check if cookbook matches your taste profile"""
        
        title_lower = book_info['title'].lower()
        author_lower = book_info['author'].lower()
        
        # Must be a cookbook
        cookbook_indicators = ['cookbook', 'recipe', 'cooking', 'kitchen', 'food', 'cuisine']
        if not any(indicator in title_lower for indicator in cookbook_indicators):
            return False
        
        # Must be in English (mostly)
        if book_info['language'] not in ['English', 'en', '']:
            return False
        
        # Must be PDF (for your processing pipeline)
        if book_info['extension'].lower() not in ['pdf']:
            return False
        
        # Relevance scoring
        relevance_score = 0
        
        # Indian cuisine bonus
        indian_keywords = ['indian', 'gujarati', 'punjabi', 'south indian', 'bengali', 'maharashtrian']
        if any(keyword in title_lower or keyword in author_lower for keyword in indian_keywords):
            relevance_score += 5
        
        # Vegetarian bonus
        veg_keywords = ['vegetarian', 'vegan', 'plant', 'jain', 'pure veg']
        if any(keyword in title_lower for keyword in veg_keywords):
            relevance_score += 3
        
        # Healthy cooking bonus
        healthy_keywords = ['healthy', 'ayurvedic', 'wellness', 'nutrition', 'superfood']
        if any(keyword in title_lower for keyword in healthy_keywords):
            relevance_score += 2
        
        # Known good authors
        good_authors = ['tarla dalal', 'sanjeev kapoor', 'madhur jaffrey', 'yamuna']
        if any(author in author_lower for author in good_authors):
            relevance_score += 4
        
        # Size filtering (reasonable cookbook size)
        try:
            size_mb = float(re.search(r'(\d+\.?\d*)', book_info['size']).group(1))
            if 'KB' in book_info['size']:
                size_mb = size_mb / 1024
            elif 'GB' in book_info['size']:
                size_mb = size_mb * 1024
            
            # Prefer 5-100MB cookbooks (good quality, not too huge)
            if 5 <= size_mb <= 100:
                relevance_score += 1
        except:
            pass
        
        return relevance_score >= 3
    
    async def download_cookbook(self, book_info: Dict) -> Optional[Path]:
        """Download cookbook PDF asynchronously"""
        
        if not book_info['download_links']:
            return None
        
        # Create safe filename
        safe_title = re.sub(r'[^\w\s-]', '', book_info['title'])
        safe_title = re.sub(r'[-\s]+', '_', safe_title)[:50]
        filename = f"{safe_title}_{book_info['year']}.pdf"
        filepath = self.data_dir / filename
        
        if filepath.exists():
            print(f"📚 Already have: {filename}")
            return filepath
        
        # Try download links
        async with httpx.AsyncClient(timeout=30) as client:
            for download_url in book_info['download_links']:
                try:
                    print(f"⬇️ Downloading: {book_info['title']}")
                    
                    # Get the actual download page
                    response = await client.get(download_url)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find direct PDF link
                    pdf_link = None
                    for link in soup.find_all('a'):
                        href = link.get('href', '')
                        if 'get.php' in href or 'download' in href:
                            if book_info['source_mirror'] not in href:
                                pdf_link = book_info['source_mirror'] + href
                            else:
                                pdf_link = href
                            break
                    
                    if pdf_link:
                        # Download the PDF
                        pdf_response = await client.get(pdf_link)
                        pdf_response.raise_for_status()
                        
                        with open(filepath, 'wb') as f:
                            f.write(pdf_response.content)
                        
                        print(f"✅ Downloaded: {filename} ({book_info['size']})")
                        return filepath
                    
                except Exception as e:
                    print(f"⚠️ Download failed for {download_url}: {e}")
                    continue
        
        return None
    
    async def harvest_cookbooks_for_nigela(self, max_per_query: int = 5, max_downloads: int = 20) -> List[Path]:
        """Main harvest function - get cookbooks matching your taste profile"""
        
        print("🌾 HARVESTING COOKBOOKS FROM LIBRARY GENESIS")
        print("=" * 60)
        
        all_books = []
        downloaded_files = []
        
        # Search for cookbooks using your taste profile
        for query in self.taste_profile_keywords[:10]:  # Limit queries
            try:
                books = self.search_cookbooks(query, max_per_query)
                all_books.extend(books)
                
                # Small delay between searches
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"⚠️ Search failed for '{query}': {e}")
        
        # Remove duplicates by title
        unique_books = {}
        for book in all_books:
            key = book['title'].lower().strip()
            if key not in unique_books:
                unique_books[key] = book
        
        print(f"📚 Found {len(unique_books)} unique relevant cookbooks")
        
        # Sort by relevance and download top ones
        sorted_books = sorted(unique_books.values(), 
                            key=lambda x: self._calculate_relevance_score(x), 
                            reverse=True)
        
        # Download top cookbooks
        download_tasks = []
        for book in sorted_books[:max_downloads]:
            task = self.download_cookbook(book)
            download_tasks.append(task)
        
        # Execute downloads concurrently (but limited)
        semaphore = asyncio.Semaphore(3)  # Max 3 concurrent downloads
        
        async def download_with_semaphore(task):
            async with semaphore:
                return await task
        
        results = await asyncio.gather(*[download_with_semaphore(task) for task in download_tasks])
        
        downloaded_files = [f for f in results if f is not None]
        
        print(f"✅ Successfully downloaded {len(downloaded_files)} cookbooks!")
        
        # Save harvest report
        self._save_harvest_report(sorted_books, downloaded_files)
        
        return downloaded_files
    
    def _calculate_relevance_score(self, book_info: Dict) -> int:
        """Calculate detailed relevance score"""
        score = 0
        title_lower = book_info['title'].lower()
        author_lower = book_info['author'].lower()
        
        # Indian cuisine (highest priority)
        if any(word in title_lower for word in ['indian', 'gujarati', 'south indian']):
            score += 10
        
        # Vegetarian (very important)
        if any(word in title_lower for word in ['vegetarian', 'vegan', 'jain']):
            score += 8
        
        # Healthy/wellness
        if any(word in title_lower for word in ['healthy', 'ayurvedic', 'wellness']):
            score += 6
        
        # Known authors
        if any(author in author_lower for author in ['tarla dalal', 'sanjeev kapoor']):
            score += 12
        
        # Recent books (more likely to have modern healthy recipes)
        try:
            year = int(book_info['year'])
            if year >= 2010:
                score += 3
            elif year >= 2000:
                score += 1
        except:
            pass
        
        return score
    
    def _save_harvest_report(self, all_books: List[Dict], downloaded_files: List[Path]):
        """Save harvest report for future reference"""
        
        report = {
            'harvest_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_books_found': len(all_books),
            'books_downloaded': len(downloaded_files),
            'downloaded_files': [str(f) for f in downloaded_files],
            'all_books': all_books[:50]  # Top 50 for reference
        }
        
        report_file = self.data_dir / 'libgen_harvest_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Harvest report saved: {report_file}")

# Integration with existing Nigela pipeline
def integrate_libgen_cookbooks_with_nigela():
    """Integrate downloaded cookbooks with Nigela's recipe processing"""
    
    print("🔗 INTEGRATING LIBGEN COOKBOOKS WITH NIGELA")
    print("=" * 50)
    
    # This will use your existing PDF processing pipeline
    from .parse_pdf import extract_dishes_from_pdf
    from .llm import parse_dish_with_ai
    from .io_xls import read_dishes, write_dishes
    
    library_dir = Path("library")
    pdf_files = list(library_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("📚 No cookbooks found. Run harvest first!")
        return
    
    print(f"📚 Processing {len(pdf_files)} cookbooks...")
    
    all_new_dishes = []
    
    for pdf_file in pdf_files:
        try:
            print(f"📖 Processing: {pdf_file.name}")
            
            # Extract text from PDF
            raw_text = extract_dishes_from_pdf(str(pdf_file))
            
            # Parse with AI (your existing pipeline)
            dishes = parse_dish_with_ai(raw_text, source=f"LibGen: {pdf_file.stem}")
            
            all_new_dishes.extend(dishes)
            
            print(f"✅ Extracted {len(dishes)} recipes from {pdf_file.name}")
            
        except Exception as e:
            print(f"⚠️ Error processing {pdf_file.name}: {e}")
    
    # Add to your dishes database
    if all_new_dishes:
        existing_dishes = read_dishes("data/dishes.xlsx")
        combined_dishes = existing_dishes + all_new_dishes
        write_dishes("data/dishes.xlsx", combined_dishes)
        
        print(f"🎉 Added {len(all_new_dishes)} new recipes to Nigela database!")
        print("🔄 New recipes will appear in your daily variety rotation!")

async def main():
    """Main function to harvest cookbooks"""
    harvester = LibgenCookbookHarvester()
    downloaded_files = await harvester.harvest_cookbooks_for_nigela(
        max_per_query=5,
        max_downloads=15  # Start with 15 high-quality cookbooks
    )
    
    if downloaded_files:
        print("\n🔗 Ready to integrate with Nigela recipe system!")
        print("Run: python3 -c 'from src.libgen_cookbook_harvester import integrate_libgen_cookbooks_with_nigela; integrate_libgen_cookbooks_with_nigela()'")

if __name__ == "__main__":
    asyncio.run(main())
