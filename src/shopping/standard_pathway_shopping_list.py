#!/usr/bin/env python3

"""
AI-Based Shopping List Generator
Generates shopping lists based on actual AI design analysis results
Uses specific product recommendations from the transformed image
"""

import json
import re
import os
from datetime import datetime
from typing import Dict, List, Any
from .shopping_list_generator import ShoppingListGenerator

class AIShoppingGenerator:
    """Generate shopping lists from AI design analysis"""
    
    def __init__(self):
        self.base_generator = ShoppingListGenerator()
    
    def generate_from_analysis(self, analysis_file: str = "design_results.json", 
                              output_filename: str = None) -> str:
        """Generate shopping list from AI analysis results"""
        
        # Load AI analysis results
        try:
            with open(analysis_file, 'r') as f:
                analysis_data = json.load(f)
        except FileNotFoundError:
            print(f"❌ Analysis file {analysis_file} not found. Run AI transformation first.")
            return None
        
        design_concept = analysis_data.get('designConcept', {})
        recommendations = analysis_data.get('recommendations', [])
        style = design_concept.get('style', 'modern').lower()
        
        print(f"🔍 Analyzing {len(recommendations)} AI recommendations for specific products...")
        
        # Extract specific products from AI recommendations
        specific_products = self.extract_products_from_ai_recommendations(recommendations, design_concept)
        
        print(f"📦 Found {len(specific_products)} specific products from AI analysis")
        for product in specific_products:
            print(f"   • {product['name']}: {product['description'][:80]}...")
        
        # Use enhanced product data generation with specific search terms
        enhanced_products = self.base_generator.generate_enhanced_product_data(specific_products, style)
        
        # Create shopping_lists directory if it doesn't exist
        shopping_lists_dir = "shopping_lists"
        if not os.path.exists(shopping_lists_dir):
            os.makedirs(shopping_lists_dir)
        
        # Generate filename
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = os.path.join(shopping_lists_dir, f"ai_analysis_shopping_{style}_{timestamp}.html")
        
        # Generate HTML
        html_content = self.base_generator.generate_html_shopping_list_with_products(
            enhanced_products, style
        )
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ AI-based shopping list saved as: {output_filename}")
        print(f"🎯 This list contains products that match what was added to your transformed image!")
        
        return output_filename
    
    def extract_products_from_ai_recommendations(self, recommendations: List[Dict], 
                                               design_concept: Dict) -> List[Dict]:
        """Extract specific products from AI recommendations with detailed specifications"""
        products = []
        
        for rec in recommendations:
            description = rec.get('description', '')
            area = rec.get('area', 'General')
            priority = rec.get('priority', 'Medium')
            
            print(f"   📝 Processing {area}: {description[:60]}...")
            
            # Parse description for specific product types
            extracted_products = self.parse_description_for_products(description, area, priority)
            products.extend(extracted_products)
        return products
    
    def parse_description_for_products(self, description: str, area: str, priority: str) -> List[Dict]:
        """Parse AI description for specific products"""
        products = []
        desc_lower = description.lower()
        
        # Product extraction patterns
        product_patterns = [
            {
                'keywords': ['pillow', 'cushion'],
                'name': 'Throw Pillows',
                'category': 'Home Decor',
                'base_search': ['throw pillows', 'decorative pillows']
            },
            {
                'keywords': ['lamp', 'lighting', 'light'],
                'name': 'Lighting',
                'category': 'Lighting',
                'base_search': ['floor lamp', 'table lamp', 'accent lighting']
            },
            {
                'keywords': ['rug', 'carpet'],
                'name': 'Area Rug',
                'category': 'Home Decor',
                'base_search': ['area rug', 'decorative rug']
            },
            {
                'keywords': ['wall hanging', 'macrame', 'art', 'prints', 'mirror'],
                'name': 'Wall Decor',
                'category': 'Wall Decor',
                'base_search': ['wall hanging', 'wall art', 'macrame']
            },
            {
                'keywords': ['vase', 'ceramic', 'pottery'],
                'name': 'Decorative Vases',
                'category': 'Home Decor',
                'base_search': ['ceramic vases', 'decorative vases']
            },
            {
                'keywords': ['candle'],
                'name': 'Candles',
                'category': 'Home Decor',
                'base_search': ['decorative candles', 'pillar candles']
            },
            {
                'keywords': ['blanket', 'throw'],
                'name': 'Throw Blanket',
                'category': 'Home Decor',
                'base_search': ['throw blanket', 'decorative throw']
            },
            {
                'keywords': ['curtain', 'drape', 'window treatment'],
                'name': 'Window Treatments',
                'category': 'Home Decor',
                'base_search': ['curtains', 'window drapes']
            },
            {
                'keywords': ['plant', 'greenery'],
                'name': 'Plants',
                'category': 'Home Decor',
                'base_search': ['indoor plants', 'decorative plants']
            },
            {
                'keywords': ['basket', 'storage'],
                'name': 'Storage Baskets',
                'category': 'Home Organization',
                'base_search': ['woven baskets', 'storage baskets']
            }
        ]
        
        # Check each pattern
        for pattern in product_patterns:
            if any(keyword in desc_lower for keyword in pattern['keywords']):
                # Build specific search terms based on AI description
                search_terms = self.build_enhanced_search_terms(
                    description, pattern['base_search']
                )
                
                product = {
                    'name': f"{area} {pattern['name']}",
                    'category': pattern['category'],
                    'description': description,
                    'area': area,
                    'priority': priority,
                    'search_terms': search_terms,
                    'specifications': self.extract_detailed_specs(description)
                }
                
                products.append(product)
                print(f"      🎯 Found: {product['name']} with {len(search_terms)} search terms")
        return products
    
    def build_enhanced_search_terms(self, description: str, base_terms: List[str]) -> List[str]:
        """Build specific search terms from AI description"""
        desc_lower = description.lower()
        enhanced_terms = []
        
        # Extract key descriptors from the AI description
        materials = self.extract_materials(description)
        colors = self.extract_colors(description)
        sizes = self.extract_sizes(description)
        styles = self.extract_styles(description)
        
        # Build enhanced search combinations
        for base_term in base_terms:
            enhanced_terms.append(base_term)
            
            # Add material combinations
            for material in materials:
                enhanced_terms.append(f"{material} {base_term}")
            
            # Add color combinations
            for color in colors:
                enhanced_terms.append(f"{color} {base_term}")
            
            # Add style combinations
            for style in styles:
                enhanced_terms.append(f"{style} {base_term}")
            
            # Add size-specific terms
            for size in sizes:
                enhanced_terms.append(f"{base_term} {size}")
        
        # Remove duplicates and limit to most specific
        unique_terms = list(set(enhanced_terms))
        return unique_terms[:6]  # Return top 6 most specific terms
    
    def extract_materials(self, text: str) -> List[str]:
        """Extract material keywords from text"""
        materials = ['rattan', 'wicker', 'linen', 'velvet', 'cotton', 'jute', 'sisal', 
                    'ceramic', 'metal', 'wood', 'macrame', 'rope', 'bamboo', 'woven']
        return [mat for mat in materials if mat in text.lower()]
    
    def extract_colors(self, text: str) -> List[str]:
        """Extract color keywords from text"""
        colors = ['terracotta', 'terra cotta', 'teal', 'mustard', 'sage', 'cream', 
                 'rust', 'navy', 'beige', 'brown', 'earthy', 'earth tone', 'warm']
        return [color for color in colors if color in text.lower()]
    
    def extract_sizes(self, text: str) -> List[str]:
        """Extract size information from text"""
        sizes = []
        
        # Look for dimension patterns
        dimension_patterns = [r'(\d+)x(\d+)', r'(\d+)\s*inch', r'(\d+)\s*feet?', r'(\d+)\s*ft']
        
        for pattern in dimension_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                sizes.append(match.group(0))
        return sizes
    
    def extract_styles(self, text: str) -> List[str]:
        """Extract style keywords from text"""
        styles = ['bohemian', 'boho', 'eclectic', 'natural', 'textured', 'vintage', 
                 'rustic', 'modern', 'contemporary', 'traditional']
        return [style for style in styles if style in text.lower()]
    
    def extract_detailed_specs(self, description: str) -> Dict[str, Any]:
        """Extract detailed specifications from AI description"""
        specs = {
            'materials': self.extract_materials(description),
            'colors': self.extract_colors(description),
            'sizes': self.extract_sizes(description),
            'styles': self.extract_styles(description)
        }
        
        # Extract quantities if mentioned
        quantity_match = re.search(r'(\d+)[ -]*(piece|pieces|set)', description.lower())
        if quantity_match:
            specs['quantity'] = quantity_match.group(1)
        return specs

def main():
    """Generate shopping list from AI analysis results"""
    
    generator = AIShoppingGenerator()
    
    print("🔍 Generating shopping list from AI transformation analysis...")
    print("   📋 Reading actual recommendations from design_results.json")
    print("   🎯 Finding specific products that match the transformed image")
    print("   🛍️ Creating accurate product links for each item")
    print()
    
    result_file = generator.generate_from_analysis()
    
    if result_file:
        print()
        print("🎉 Success! Your AI-based shopping list is ready!")
        print(f"📂 File: {result_file}")
        print("🛒 Each product now matches what was actually added to your transformed image!")
        print()
        print("Key improvements:")
        print("  • Products based on actual AI transformation recommendations")
        print("  • Specific search terms extracted from AI analysis")
        print("  • Material, color, and size details from the transformation")
        print("  • Direct links to products that match your redesign")
    
if __name__ == "__main__":
    main() 