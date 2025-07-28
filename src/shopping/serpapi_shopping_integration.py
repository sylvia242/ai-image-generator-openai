#!/usr/bin/env python3
"""
SerpAPI Google Shopping Integration
Searches for real products and downloads images for AI design composition
"""

import os
import requests
import time
from datetime import datetime
from typing import List, Dict, Optional

class SerpAPIShopping:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('SERPAPI_KEY')
        if not self.api_key:
            raise ValueError("SERPAPI_KEY not found in environment variables")
    
    def search_products(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for products using SerpAPI Google Shopping"""
        
        url = "https://serpapi.com/search"
        params = {
            'api_key': self.api_key,
            'engine': 'google_shopping',
            'q': query,
            'num': max_results,
            'gl': 'us',
            'hl': 'en'
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            print(f"   🔍 API Response keys: {list(data.keys())}")
            
            if 'shopping_results' not in data:
                print(f"   ❌ No shopping results found for: {query}")
                print(f"   📊 Available keys: {list(data.keys())}")
                return []
            
            print(f"   📊 Shopping results count: {len(data['shopping_results'])}")
            
            # Debug: Check first result structure
            if data['shopping_results']:
                first_result = data['shopping_results'][0]
                print(f"   🔍 First result keys: {list(first_result.keys())}")
                print(f"   📝 First result title: {first_result.get('title', 'No title')}")
                print(f"   🔗 First result link: {first_result.get('link', 'No link')}")
            
            results = []
            for item in data['shopping_results'][:max_results]:
                parsed = self.parse_serpapi_result(item, query)
                if parsed:
                    results.append(parsed)
            
            print(f"   ✅ Found {len(results)} products for: {query}")
            return results
            
        except Exception as e:
            print(f"   ❌ Error searching SerpAPI: {e}")
            return []
    
    def parse_serpapi_result(self, item: Dict, original_query: str) -> Optional[Dict]:
        """Parse SerpAPI shopping result"""
        
        try:
            # Extract basic info using correct field names
            title = item.get('title', '')
            link = item.get('product_link', '')  # Changed from 'link' to 'product_link'
            price = self.parse_price(item.get('price', ''))
            rating = item.get('rating')
            reviews = item.get('reviews')
            thumbnail = item.get('thumbnail')  # Changed from 'image' to 'thumbnail'
            source = item.get('source', 'Unknown')
            
            # Skip if no essential data
            if not title or not link:
                return None
            
            return {
                'name': title,
                'url': link,
                'price': price,
                'rating': rating,
                'reviews': reviews,
                'image': thumbnail,
                'retailer': source
            }
            
        except Exception as e:
            print(f"   ❌ Error parsing result: {e}")
            return None
    
    def parse_price(self, price_str: str) -> Optional[float]:
        """Parse price string to float"""
        if not price_str:
            return None
        
        try:
            # Remove currency symbols and convert to float
            clean_price = price_str.replace('$', '').replace(',', '').strip()
            return float(clean_price)
        except:
            return None
    
    def search_interior_products(self, product_type: str, style: str = "bohemian", 
                               colors: List[str] = None) -> List[Dict]:
        """
        Search for interior design products with style and color preferences
        Limited to 15 products maximum for better performance
        """
        colors = colors or []
        
        # Build search query
        color_terms = " ".join(colors[:2]) if colors else ""
        query = f"{style} {product_type} {color_terms}".strip()
        
        # Add product-specific terms for better results
        product_enhancements = {
            'throw pillows': 'decorative cushions',
            'floor lamp': 'lighting fixture',
            'wall art': 'wall hanging decor',
            'ceramic vases': 'pottery decorative',
            'area rug': 'decorative carpet',
            'curtains': 'window treatments',
            'candles': 'decorative candles',
            'plants': 'indoor plants',
            'throw blanket': 'textile decorative'
        }
        
        enhancement = product_enhancements.get(product_type.lower(), "")
        if enhancement:
            query = f"{query} {enhancement}"
        
        # Limit to 15 products maximum for better performance
        return self.search_products(query, max_results=15)
    
    def download_product_image(self, image_url: str, product_name: str, output_dir: str = None) -> Optional[str]:
        """
        Download product image and save locally
        Returns local file path if successful
        """
        if not image_url:
            return None
        
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Create filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')[:30]
            filename = f"serpapi_product_{safe_name}_{timestamp}.jpg"
            
            # Save image in specified directory or current directory
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                filepath = os.path.join(output_dir, filename)
            else:
                filepath = filename
            
            # Save image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"   📸 Downloaded: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"   ❌ Failed to download image: {e}")
            return None

def test_serpapi_shopping():
    """Test SerpAPI Google Shopping integration"""
    
    api = SerpAPIShopping()
    
    # Test product searches
    test_products = [
        "bohemian throw pillows",
        "rattan floor lamp",
        "macrame wall hanging",
        "ceramic decorative vases"
    ]
    
    print("🧪 Testing SerpAPI Google Shopping Integration...")
    print("   🔍 Searching for real interior design products")
    print("   📸 Downloading actual product images")
    print("   🛒 Getting real product URLs and prices")
    print()
    
    for product_query in test_products:
        print(f"🔍 Testing: {product_query}")
        
        products = api.search_products(product_query, max_results=2)
        
        for i, product in enumerate(products, 1):
            print(f"   {i}. {product['name'][:50]}...")
            print(f"      💰 Price: ${product['price']}" if product['price'] else "      💰 Price: Not available")
            print(f"      🏪 Retailer: {product['retailer']}")
            print(f"      ⭐ Rating: {product.get('rating', 'N/A')} ({product.get('reviews', 'N/A')} reviews)")
            print(f"      🔗 URL: {product['url'][:60]}...")
            
            if product['image']:
                local_path = api.download_product_image(product['image'], product['name'])
                if local_path:
                    print(f"      📸 Image: {local_path}")
            
            print()
        
        time.sleep(1)  # Be respectful to API limits

if __name__ == "__main__":
    test_serpapi_shopping() 