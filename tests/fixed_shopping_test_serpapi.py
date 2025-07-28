#!/usr/bin/env python3

"""
Simple test to show how individual product URLs should work
"""

import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.shopping.shopping_list_generator import ShoppingListGenerator

def test_individual_products():
    """Test that shows how individual products should be found"""
    
    generator = ShoppingListGenerator()
    
    # Test product normalization
    test_names = [
        "Seating Area Throw Pillows",
        "Lighting Lighting", 
        "Accessories Decorative Vases",
        "Walls and Decor Wall Decor"
    ]
    
    print("🧪 Testing Product Name Processing:")
    for name in test_names:
        # Simple name processing for display
        processed = name.replace(" Area", "").replace(" and ", " ").replace("Decor ", "")
        print(f"   '{name}' → '{processed}'")
    
    print("\n🔍 Testing Individual Product Search:")
    
    # Test direct product lookup
    retailer_info = {
        'name': 'Amazon',
        'logo': 'https://example.com/amazon-logo.png'
    }
    
    test_products = ['throw pillows', 'lighting', 'decorative vases', 'wall decor']
    
    for product_name in test_products:
        print(f"\n   Testing: {product_name}")
        result = generator.find_specific_product("", retailer_info, product_name)
        
        if result:
            print(f"   ✅ Found: {result['name']}")
            print(f"   🔗 URL: {result['url']}")
            print(f"   💰 Price: ${result['price']}")
        else:
            print(f"   ❌ Not found")

if __name__ == "__main__":
    test_individual_products() 