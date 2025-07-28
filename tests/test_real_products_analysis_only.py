#!/usr/bin/env python3
"""
Test Script: Real Products Pathway - Analysis & Shopping List Only
Tests the analysis and shopping list generation without creating the final image
"""

import sys
import os
import json
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.real_products_pathway import RealProductsPathway
from src.shopping.serpapi_shopping_integration import SerpAPIShopping
from src.shopping.real_products_pathway_shopping_list import create_serpapi_shopping_list
from config.config_settings import get_api_key, get_serpapi_key


def test_real_products_analysis_and_shopping():
    """Test the analysis and shopping list generation parts of real products pathway"""
    
    print("🧪 TESTING REAL PRODUCTS PATHWAY - ANALYSIS & SHOPPING ONLY")
    print("="*70)
    
    # Check API keys
    openai_key = get_api_key()
    serpapi_key = get_serpapi_key()
    
    if not openai_key:
        print("❌ Error: OpenAI API key not found")
        return False
    
    if not serpapi_key:
        print("❌ Error: SerpAPI key not found")
        return False
    
    print("✅ API keys configured")
    
    # Initialize the real products pathway
    real_products_pathway = RealProductsPathway(openai_key)
    
    # Test image path (using user's specified image)
    test_image_path = "/Users/sylviaschumacher/Desktop/Screenshot 2025-07-27 at 7.27.58 PM.png"
    
    if not os.path.exists(test_image_path):
        print(f"❌ Error: Test image '{test_image_path}' not found")
        print("   Please check the image path and ensure the file exists")
        return False
    
    print(f"✅ Test image found: {test_image_path}")
    
    try:
        # Step 1: Analyze the image
        print("\n🔍 STEP 1: Analyzing image with GPT-4o Vision...")
        analysis_results = real_products_pathway.analyze_image(
            image_path=test_image_path,
            design_style="modern",
            custom_instructions="Add clean lines, minimalist decor, and contemporary styling",
            design_type="interior redesign"
        )
        
        if not analysis_results:
            print("❌ Error: Image analysis failed")
            return False
        
        print("✅ Image analysis completed successfully!")
        
        # Display analysis results
        design_concept = analysis_results.get('designConcept', {})
        recommendations = analysis_results.get('recommendations', [])
        
        print(f"\n📊 ANALYSIS RESULTS:")
        print(f"   🎨 Style: {design_concept.get('style', 'Unknown')}")
        print(f"   🎨 Color Palette: {', '.join(design_concept.get('colorPalette', []))}")
        print(f"   📋 Recommendations: {len(recommendations)}")
        
        # Show first few recommendations
        for i, rec in enumerate(recommendations[:3], 1):
            priority = rec.get('priority', 'Unknown')
            area = rec.get('area', 'General')
            description = rec.get('description', 'No description')[:80]
            print(f"   {i}. [{priority}] {area}: {description}...")
        
        # Step 2: Search for real products
        print("\n🛒 STEP 2: Searching for real products using SerpAPI...")
        
        serpapi_shopping = SerpAPIShopping(serpapi_key)
        real_products_with_images = []
        
        # Extract recommendations and color palette
        color_palette = analysis_results.get('colorPalette', {}).get('primary', [])
        
        for product in recommendations:
            print(f"   🔍 Searching for: {product['type']}")
            
            # Search for real products
            search_results = serpapi_shopping.search_interior_products(
                product_type=product['type'],
                style="modern",
                colors=color_palette
            )
            
            if search_results:
                # Take the first product with an image
                for real_product in search_results:
                    image_url = real_product.get('image')
                    if image_url:
                        # Download the product image
                        local_image_path = serpapi_shopping.download_product_image(
                            image_url, real_product['name']
                        )
                        
                        if local_image_path:
                            # Update product info
                            real_product['permanent_image_path'] = local_image_path
                            real_product['area'] = product['area']
                            real_product['product_url'] = real_product.get('url', '')
                            real_products_with_images.append(real_product)
                            print(f"   ✅ Found: {real_product['name']} (${real_product.get('price', 'N/A')})")
                            break
                        else:
                            print(f"   ❌ No image downloaded for: {real_product['name']}")
                    else:
                        print(f"   ❌ No image available for: {real_product['name']}")
            else:
                print(f"   ❌ No products found for: {product['type']}")
        
        if not real_products_with_images:
            print("❌ Error: No real products with images found")
            return False
        
        print(f"\n✅ Found {len(real_products_with_images)} products with images")
        
        # Step 3: Generate shopping list
        print("\n📝 STEP 3: Generating shopping list...")
        
        # Save analysis results to JSON for shopping list generation
        analysis_file = "test_analysis_results.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis_results, f, indent=2)
        
        # Create a results file that includes the real products data
        results_data = {
            'serpapiProductsComposition': {
                'products_info': [
                    {
                        'name': p['name'],
                        'area': p['area'],
                        'product_url': p.get('url', ''),
                        'price': p.get('price'),
                        'retailer': p.get('retailer'),
                        'rating': p.get('rating'),
                        'reviews': p.get('reviews'),
                        'permanent_image_path': p.get('permanent_image_path', '')
                    } for p in real_products_with_images
                ]
            }
        }
        
        # Save results to JSON file
        results_file = "test_design_results.json"
        with open(results_file, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        # Generate the shopping list HTML
        output_file = create_serpapi_shopping_list(results_file)
        
        if output_file:
            print(f"✅ Shopping list generated: {output_file}")
            print(f"✅ Analysis results saved: {analysis_file}")
            print(f"✅ Design results saved: {results_file}")
            
            # Display summary
            print(f"\n📊 TEST SUMMARY:")
            print(f"   🔍 Analysis: ✅ Completed")
            print(f"   🛒 Product Search: ✅ Found {len(real_products_with_images)} products")
            print(f"   📝 Shopping List: ✅ Generated")
            print(f"   🖼️  Image Generation: ⏭️  Skipped (as requested)")
            
            print(f"\n🌐 Open {output_file} in your browser to see the shopping list!")
            print(f"📄 Analysis details saved in {analysis_file}")
            
            return True
        else:
            print("❌ Error: Failed to generate shopping list")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        return False


def main():
    """Main test function"""
    print("🧪 REAL PRODUCTS PATHWAY - ANALYSIS & SHOPPING TEST")
    print("="*70)
    print("This test covers:")
    print("   ✅ Image analysis with GPT-4o Vision")
    print("   ✅ Product search with SerpAPI")
    print("   ✅ Shopping list generation")
    print("   ⏭️  Image generation (skipped)")
    print()
    
    success = test_real_products_analysis_and_shopping()
    
    if success:
        print("\n🎉 TEST COMPLETED SUCCESSFULLY!")
        print("   All analysis and shopping list generation steps passed")
    else:
        print("\n❌ TEST FAILED!")
        print("   Check the error messages above")


if __name__ == "__main__":
    main() 