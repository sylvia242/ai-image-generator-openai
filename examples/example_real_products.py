#!/usr/bin/env python3
"""
Example script showing Real Products Pathway - complete pipeline with image generation
"""

import sys
import os
import json
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.real_products_pathway import RealProductsPathway
from config.config_settings import get_api_key, get_serpapi_key


def main():
    """Demonstrate Real Products Pathway - complete pipeline with image generation"""
    
    print("🎨 REAL PRODUCTS PATHWAY - COMPLETE PIPELINE")
    print("="*60)
    
    # Check API keys
    openai_key = get_api_key()
    serpapi_key = get_serpapi_key()
    
    if not openai_key:
        print("❌ Error: OpenAI API key not found")
        return
    
    if not serpapi_key:
        print("❌ Error: SerpAPI key not found")
        return
    
    print("✅ API keys configured")
    
    # Initialize the real products pathway
    real_products_pathway = RealProductsPathway(openai_key)
    
    # Test image path (you can change this to your test image)
    test_image_path = "/Users/sylviaschumacher/Desktop/Screenshot 2025-07-27 at 7.27.58 PM.png"
    
    if not os.path.exists(test_image_path):
        print(f"❌ Error: Test image '{test_image_path}' not found")
        print("   Please update the test_image_path variable to point to your image")
        return
    
    print(f"✅ Test image found: {test_image_path}")
    
    try:
        print("\n🚀 Starting Real Products Pathway Pipeline...")
        print("   🔍 Step 1: Analyze image with GPT-4o Vision")
        print("   🛒 Step 2: Search for real products with SerpAPI")
        print("   📝 Step 3: Generate shopping list")
        print("   🎨 Step 4: Generate final image with real products")
        
        # Step 1: Analyze the image
        print("\n🔍 STEP 1: Analyzing image with GPT-4o Vision...")
        analysis_results = real_products_pathway.analyze_image(
            image_path=test_image_path,
            design_style="scandinavian",
            custom_instructions="Add clean lines, minimalist decor, and contemporary styling",
            design_type="interior redesign"
        )
        
        if not analysis_results:
            print("❌ Error: Image analysis failed")
            return
        
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
        
        # Step 2: Generate design with real products (includes product search and image generation)
        print("\n🎨 STEP 2: Generating design with real products...")
        print("   🛒 Searching for real products using SerpAPI...")
        print("   🎨 Creating final image with GPT Image 1...")
        
        final_results = real_products_pathway.generate_design_with_real_products(
            image_path=test_image_path,
            design_style="scandinavian",
            custom_instructions="Add clean lines, minimalist decor, and contemporary styling",
            design_type="interior redesign",
            serpapi_key=serpapi_key
        )
        
        if not final_results:
            print("❌ Error: Design generation failed")
            return
        
        print("✅ Design generation completed successfully!")
        
        # Display final results
        if 'serpapiProductsComposition' in final_results:
            comp_info = final_results['serpapiProductsComposition']
            products_used = comp_info.get('products_used', 0)
            final_image = comp_info.get('final_image', {})
            
            print(f"\n📊 FINAL RESULTS:")
            print(f"   🛒 Products Used: {products_used}")
            print(f"   🎨 Final Image: {final_image.get('filename', 'Unknown')}")
            print(f"   🛤️  Method: {comp_info.get('method', 'Unknown')}")
            
            # Show product details
            products_info = comp_info.get('products_info', [])
            if products_info:
                print(f"\n🛒 PRODUCTS USED:")
                for i, product in enumerate(products_info[:5], 1):
                    name = product.get('name', 'Unknown')
                    price = product.get('price', 'Unknown')
                    retailer = product.get('retailer', 'Unknown')
                    print(f"   {i}. {name} - ${price} ({retailer})")
        
        # Step 3: Generate shopping list
        print("\n📝 STEP 3: Generating shopping list...")
        
        # Save results to JSON file for shopping list generation
        results_file = "example_real_products_results.json"
        with open(results_file, 'w') as f:
            json.dump(final_results, f, indent=2)
        
        # Import and use the shopping list function
        from src.shopping.real_products_pathway_shopping_list import create_serpapi_shopping_list
        
        # Generate the shopping list HTML
        shopping_list_file = create_serpapi_shopping_list(results_file)
        
        if shopping_list_file:
            print(f"✅ Shopping list generated: {shopping_list_file}")
        
        # Display summary
        print(f"\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"   🔍 Analysis: ✅ Completed")
        print(f"   🛒 Product Search: ✅ Completed")
        print(f"   📝 Shopping List: ✅ Generated")
        print(f"   🎨 Final Image: ✅ Generated")
        
        print(f"\n📁 Generated Files:")
        print(f"   📄 Analysis: {results_file}")
        print(f"   🛒 Shopping List: {shopping_list_file}")
        if 'serpapiProductsComposition' in final_results:
            final_image = final_results['serpapiProductsComposition'].get('final_image', {})
            print(f"   🎨 Final Image: {final_image.get('filename', 'Unknown')}")
        
        print(f"\n🌐 Open {shopping_list_file} in your browser to see the shopping list!")
        print("🎨 The final image shows your room with the real products integrated!")
        
    except Exception as e:
        print(f"❌ Error during pipeline: {str(e)}")


if __name__ == "__main__":
    main() 