#!/usr/bin/env python3
"""
Example script showing enhanced shopping list generation with real product discovery
"""

from src.shopping.shopping_list_generator import ShoppingListGenerator

def main():
    """Demonstrate enhanced shopping list generation with real products"""
    
    # Sample AI design analysis (what your AI would generate)
    design_analysis = {
        'designConcept': {
            'style': 'bohemian',
            'colorPalette': ['terracotta', 'teal', 'cream', 'warm brown'],
            'materials': ['rattan', 'ceramic', 'natural wood', 'woven textiles']
        },
        'recommendations': [
            {
                'area': 'Seating Area',
                'description': 'Add bohemian throw pillows in terracotta and teal colors',
                'priority': 'High'
            },
            {
                'area': 'Lighting',
                'description': 'Modern floor lamp with rattan shade and wooden base',
                'priority': 'High'
            },
            {
                'area': 'Wall Decor',
                'description': 'Macramé wall hanging or bohemian-style artwork',
                'priority': 'Medium'
            },
            {
                'area': 'Coffee Table',
                'description': 'Handcrafted ceramic vases in earth tones',
                'priority': 'Medium'
            }
        ]
    }
    
    # Product recommendations from your AI
    sample_products = [
        {'name': 'Throw pillows', 'priority': 'High', 'area': 'Seating Area'},
        {'name': 'Floor lamp', 'priority': 'High', 'area': 'Lighting'},
        {'name': 'Wall art', 'priority': 'Medium', 'area': 'Wall Decor'},
        {'name': 'Ceramic vases', 'priority': 'Medium', 'area': 'Coffee Table'},
        {'name': 'Area rug', 'priority': 'Low', 'area': 'Floor'}
    ]
    
    # Initialize the enhanced shopping list generator
    generator = ShoppingListGenerator()
    
    print("🔍 Generating enhanced shopping list with real product discovery...")
    print("   ✨ Searching for individual products that match your AI design")
    print("   🎯 Using actual product URLs instead of generic search results")
    print("   🛍️ Integrating with Amazon, Target, and other retailers")
    
    # Generate shopping list with real product discovery
    output_file = generator.save_shopping_list(
        products=sample_products,
        style="bohemian",
        image_filename="comprehensive_variation_20250725_184521.png",
        output_filename="enhanced_shopping_list_bohemian.html",
        design_analysis=design_analysis
    )
    
    print(f"\n✅ Enhanced shopping list saved as: {output_file}")
    print("\n🎉 Key improvements:")
    print("   • Real product URLs instead of generic search links")
    print("   • Specific product names and descriptions")
    print("   • Actual prices and ratings from retailers")
    print("   • Enhanced matching based on AI color/material analysis")
    print("   • Curated products that match your generated design")
    
    print(f"\n🌐 Open {output_file} in your browser to see the enhanced shopping experience!")
    print("\nNow each product links to a specific item you can actually buy! 🛒")

if __name__ == "__main__":
    main() 