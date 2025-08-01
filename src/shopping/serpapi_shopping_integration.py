#!/usr/bin/env python3
"""
SerpAPI Google Shopping Integration
Searches for real products and downloads images for AI design composition
"""

import os
import requests
import time
import random
from datetime import datetime
from typing import List, Dict, Optional
import re # Added for regex in product description parsing

class SerpAPIShopping:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('SERPAPI_KEY')
        if not self.api_key:
            raise ValueError("SERPAPI_KEY not found in environment variables")
        
        # Create a session for connection reuse
        self.session = requests.Session()
        # Configure session for better performance
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        # Enable connection pooling
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=3
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
    
    def search_products(self, query: str, max_results: int = 5, price_range: str = None, sort_by: str = "popularity") -> List[Dict]:
        """Search for products using SerpAPI Google Shopping with enhanced parameters"""
        
        url = "https://serpapi.com/search"
        params = {
            'api_key': self.api_key,
            'engine': 'google_shopping',
            'q': query,
            'num': max_results,
            'gl': 'us',
            'hl': 'en',
            'sort': sort_by  # popularity, price_low, price_high, rating
        }
        
        # Add price range filtering
        if price_range:
            if price_range == "budget":
                params['price_low'] = 1
                params['price_high'] = 50
            elif price_range == "affordable":
                params['price_low'] = 25
                params['price_high'] = 150
            elif price_range == "premium":
                params['price_low'] = 100
                params['price_high'] = 500
            elif price_range == "luxury":
                params['price_low'] = 300
                params['price_high'] = 2000
        
        try:
            response = self.session.get(url, params=params, timeout=30)
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
            # Extract basic product information
            title = item.get('title', '')
            price = item.get('extracted_price', item.get('price', 'N/A'))
            retailer = item.get('source', 'Unknown')
            
            # Extract the actual product URL (not just Google Shopping)
            product_url = item.get('product_link', '')
            if not product_url:
                # Try alternative URL fields
                product_url = item.get('link', '')
            
            # Extract rating and reviews
            rating = item.get('rating')
            reviews = item.get('reviews')
            
            # Convert rating to float if it's a string
            if isinstance(rating, str):
                try:
                    rating = float(rating)
                except:
                    rating = None
            
            # Convert reviews to int if it's a string
            if isinstance(reviews, str):
                try:
                    reviews = int(reviews.replace(',', ''))
                except:
                    reviews = None
            
            # Extract image URL
            image_url = None
            if 'thumbnail' in item:
                image_url = item['thumbnail']
            elif 'thumbnails' in item and item['thumbnails']:
                image_url = item['thumbnails'][0]
            
            return {
                'name': title,
                'price': f"${price}" if price != 'N/A' else 'N/A',
                'retailer': retailer,
                'url': product_url,
                'rating': rating,
                'reviews': reviews,
                'image_url': image_url,
                'original_query': original_query
            }
            
        except Exception as e:
            print(f"   ⚠️  Error parsing SerpAPI result: {e}")
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
    
    def generate_search_queries_from_analysis(self, analysis_results: Dict, product_type: str, style: str, colors: List[str] = None, product_description: str = None) -> List[str]:
        """Generate diverse search queries based on GPT-4 Vision analysis and product description"""
        queries = []
        colors = colors or []
        
        # Extract key insights from analysis
        room_type = analysis_results.get('room_type', 'room')
        existing_furniture = analysis_results.get('existing_furniture', [])
        color_scheme = analysis_results.get('color_scheme', colors)
        mood = analysis_results.get('mood', '')
        style_details = analysis_results.get('style_details', [])
        
        # Extract key specifications from product description
        description_keywords = []
        if product_description:
            # Extract size specifications
            size_patterns = [
                r'(\d+[x×]\d+)\s*(?:inches?|cm|feet?)',  # "18x18 inches", "24x36 cm"
                r'(\d+)\s*(?:inches?|cm|feet?)\s*(?:tall|high|wide|long)',  # "60 inches tall"
                r'(\d+)\s*(?:inch|cm|foot)\s*(?:diameter|width|height)',  # "12 inch diameter"
            ]
            
            for pattern in size_patterns:
                matches = re.findall(pattern, product_description.lower())
                description_keywords.extend(matches)
            
            # Extract material specifications
            material_patterns = [
                r'(cotton|linen|velvet|silk|wool|leather|rattan|ceramic|glass|metal|wood|plastic|fabric)',
                r'(organic|natural|synthetic|premium|luxury|textured|smooth|matte|glossy)',
                r'(tufted|embroidered|woven|knitted|printed|painted|carved|molded)'
            ]
            
            for pattern in material_patterns:
                matches = re.findall(pattern, product_description.lower())
                description_keywords.extend(matches)
            
            # Extract color specifications
            color_patterns = [
                r'(terracotta|sage|cream|rust|teal|navy|charcoal|beige|brown|gray|white|black|gold|silver)',
                r'(earth tones?|neutral|warm|cool|pastel|vibrant|muted)'
            ]
            
            for pattern in color_patterns:
                matches = re.findall(pattern, product_description.lower())
                description_keywords.extend(matches)
            
            # Extract style specifications
            style_patterns = [
                r'(bohemian|modern|traditional|scandinavian|minimalist|industrial|coastal|mid-century|contemporary)',
                r'(geometric|floral|abstract|geometric|organic|symmetric|asymmetric)',
                r'(tassel|fringe|trim|border|pattern|design|motif)'
            ]
            
            for pattern in style_patterns:
                matches = re.findall(pattern, product_description.lower())
                description_keywords.extend(matches)
            
            # Remove duplicates and limit
            description_keywords = list(set(description_keywords))[:5]
            print(f"   🔍 Extracted keywords from description: {description_keywords}")
        
        # Base query variations
        base_variations = [
            f"{style} {product_type}",
            f"{product_type} {style} decor",
            f"{product_type} {style} home",
            f"best {product_type} {style}",
            f"{style} {product_type} {room_type}"
        ]
        
        # Add description-based variations
        if description_keywords:
            for keyword in description_keywords:
                desc_variations = [
                    f"{style} {product_type} {keyword}",
                    f"{product_type} {keyword} {style}",
                    f"{keyword} {product_type} {style}",
                    f"{style} {keyword} {product_type}"
                ]
                base_variations.extend(desc_variations)
        
        # Add color variations
        if colors:
            color_terms = " ".join(colors[:2])
            color_variations = [
                f"{style} {product_type} {color_terms}",
                f"{product_type} {color_terms} {style}",
                f"{style} {color_terms} {product_type}"
            ]
            base_variations.extend(color_variations)
        
        # Add mood-based variations
        if mood:
            mood_variations = [
                f"{mood} {style} {product_type}",
                f"{product_type} {mood} {style}",
                f"{style} {product_type} {mood}"
            ]
            base_variations.extend(mood_variations)
        
        # Add style detail variations
        if style_details:
            for detail in style_details[:2]:  # Use top 2 style details
                detail_variations = [
                    f"{detail} {product_type} {style}",
                    f"{style} {product_type} {detail}",
                    f"{product_type} {detail} {style}"
                ]
                base_variations.extend(detail_variations)
        
        # Add product-specific enhancements
        product_enhancements = {
            'throw pillows': ['decorative cushions', 'accent pillows', 'sofa pillows'],
            'floor lamp': ['lighting fixture', 'table lamp', 'ambient lighting'],
            'wall art': ['wall hanging decor', 'canvas art', 'gallery wall'],
            'ceramic vases': ['pottery decorative', 'flower vase', 'centerpiece'],
            'area rug': ['decorative carpet', 'floor covering', 'accent rug'],
            'curtains': ['window treatments', 'drapes', 'window coverings'],
            'candles': ['decorative candles', 'scented candles', 'ambient lighting'],
            'plants': ['indoor plants', 'houseplants', 'potted plants'],
            'throw blanket': ['textile decorative', 'throw', 'blanket']
        }
        
        enhancements = product_enhancements.get(product_type.lower(), [])
        for enhancement in enhancements:
            enhancement_variations = [
                f"{style} {enhancement}",
                f"{enhancement} {style}",
                f"{style} {product_type} {enhancement}"
            ]
            base_variations.extend(enhancement_variations)
        
        # Add brand/style combinations for more variety
        style_brands = {
            'modern': ['west elm', 'cb2', 'design within reach'],
            'bohemian': ['anthropologie', 'urban outfitters', 'world market'],
            'scandinavian': ['ikea', 'hay', 'muuto'],
            'traditional': ['pottery barn', 'crate and barrel', 'restoration hardware'],
            'minimalist': ['muji', 'hay', 'normann copenhagen']
        }
        
        brands = style_brands.get(style.lower(), [])
        for brand in brands:
            brand_variations = [
                f"{brand} {product_type}",
                f"{product_type} {brand}",
                f"{style} {brand} {product_type}"
            ]
            base_variations.extend(brand_variations)
        
        # Remove duplicates and limit to reasonable number
        unique_queries = list(set(base_variations))
        return unique_queries[:20]  # Increased limit to accommodate description-based queries
    
    def search_interior_products_with_variation(self, product_type: str, style: str = "bohemian", 
                                             colors: List[str] = None, room_analysis: Dict = None,
                                             max_results: int = 10, price_range: str = None, 
                                             sort_by: str = "popularity") -> List[Dict]:
        """
        Search for interior design products with enhanced variation
        Uses multiple search queries and price ranges for better variety
        """
        colors = colors or []
        
        all_results = []
        
        # Generate diverse search queries
        if room_analysis:
            search_queries = self.generate_search_queries_from_analysis(
                room_analysis, product_type, style, colors
            )
        else:
            # Fallback to basic queries
            color_terms = " ".join(colors[:2]) if colors else ""
            search_queries = [f"{style} {product_type} {color_terms}".strip()]
        
        print(f"   🔍 Generated {len(search_queries)} search variations for {product_type}")
        
        # Try different queries
        for query in search_queries[:3]:  # Limit to top 3 queries
            print(f"   🔍 Searching: '{query}'")
            
            results = self.search_products(
                query=query, 
                max_results=max_results,
                price_range=price_range,
                sort_by=sort_by
            )
            
            all_results.extend(results)
            
            # Early exit if we have enough products
            if len(all_results) >= max_results:
                break
        
        # Remove duplicates based on product name
        seen_names = set()
        unique_results = []
        for result in all_results:
            if result['name'] not in seen_names:
                seen_names.add(result['name'])
                unique_results.append(result)
        
        print(f"   ✅ Found {len(unique_results)} unique products for {product_type}")
        return unique_results[:max_results]  # Return requested number of products
    
    def search_interior_products(self, product_type: str, style: str = "bohemian", 
                               colors: List[str] = None) -> List[Dict]:
        """
        Legacy method - now calls the enhanced version
        Limited to 15 products maximum for better performance
        """
        return self.search_interior_products_with_variation(
            product_type=product_type,
            style=style,
            colors=colors
        )
    
    def download_product_image(self, result_or_url, product_name: str = None, output_dir: str = None) -> Optional[str]:
        """Download product image and save to local directory"""
        
        # Handle both result object and direct URL
        if isinstance(result_or_url, dict):
            # Called with result object
            result = result_or_url
            image_url = result.get('image_url', result.get('thumbnail'))
            product_name = result.get('name', 'Unknown Product')
        else:
            # Called with direct URL
            image_url = result_or_url
            if not product_name:
                product_name = 'Unknown Product'
        
        if not image_url:
            return None
            
        try:
            # Clean product name for filename
            safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')[:50]  # Limit length
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"serpapi_product_{safe_name}_{timestamp}.jpg"
            
            # Use provided output directory or default
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                filepath = os.path.join(output_dir, filename)
            else:
                filepath = filename
            
            # Download image using session for connection reuse
            response = self.session.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Save image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"   📸 Downloaded: {os.path.basename(filepath)}")
            return filepath
            
        except Exception as e:
            print(f"   ❌ Error downloading image for {product_name}: {e}")
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
            
            if product['image_url']:
                local_path = api.download_product_image(product['image_url'], product['name'])
                if local_path:
                    print(f"      📸 Image: {local_path}")
            
            print()
        
        time.sleep(1)  # Be respectful to API limits

if __name__ == "__main__":
    test_serpapi_shopping() 