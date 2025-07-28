#!/usr/bin/env python3
"""
Test script to demonstrate both pathways of the AI Image Generator
"""

import os
from config.config_settings import get_api_key, get_serpapi_key
from src.core.ai_image_generator import AIImageGenerator

def test_standard_pathway(image_path: str):
    """Test the standard pathway (AI imagined products)"""
    print("🎨 TESTING STANDARD PATHWAY")
    print("="*50)
    
    api_key = get_api_key()
    if not api_key:
        print("❌ No API key found")
        return
    
    generator = AIImageGenerator(api_key)
    
    try:
        results = generator.generate_design(
            image_path=image_path,
            design_style="modern",
            custom_instructions="Add clean lines, minimalist decor, and contemporary styling",
            design_type="interior redesign",
            edit_mode="edit"
        )
        
        # Save results
        generator.save_results(results, "standard_pathway_results.json")
        print("✅ Standard pathway completed!")
        
        return results
        
    except Exception as e:
        print(f"❌ Standard pathway error: {str(e)}")
        return None

def test_real_products_pathway(image_path: str):
    """Test the real products pathway"""
    print("\n🛒 TESTING REAL PRODUCTS PATHWAY")
    print("="*50)
    
    api_key = get_api_key()
    if not api_key:
        print("❌ No API key found")
        return
    
    generator = AIImageGenerator(api_key)
    
    try:
        results = generator.generate_design_with_real_products(
            image_path=image_path,
            design_style="modern",
            custom_instructions="Add clean lines, minimalist decor, and contemporary styling",
            design_type="interior redesign"
        )
        
        # Save results
        generator.save_results(results, "real_products_pathway_results.json")
        print("✅ Real products pathway completed!")
        
        return results
        
    except Exception as e:
        print(f"❌ Real products pathway error: {str(e)}")
        return None

def main():
    """Main test function"""
    # Use the local test image
    image_path = "test_image.png"
    
    if not os.path.exists(image_path):
        print(f"❌ Test image not found: {image_path}")
        print("Please update the image_path in the script")
        return
    
    print("🧪 AI IMAGE GENERATOR PATHWAY TESTING")
    print("="*60)
    print(f"📸 Test image: {image_path}")
    print()
    
    # Test standard pathway
    standard_results = test_standard_pathway(image_path)
    
    # Test real products pathway
    real_products_results = test_real_products_pathway(image_path)
    
    # Compare results
    print("\n📊 COMPARISON")
    print("="*50)
    
    if standard_results:
        print("✅ Standard pathway: SUCCESS")
        if 'transformedImage' in standard_results:
            print(f"   📁 Generated: {standard_results['transformedImage']['filename']}")
    else:
        print("❌ Standard pathway: FAILED")
    
    if real_products_results:
        print("✅ Real products pathway: SUCCESS")
        if 'realProductsComposition' in real_products_results:
            composition = real_products_results['realProductsComposition']
            print(f"   📁 Generated: {composition['final_image']['filename']}")
            print(f"   🛒 Products used: {composition['products_used']}")
            for product in composition['products_info']:
                print(f"      • {product['name']} ({product['area']})")
    else:
        print("❌ Real products pathway: FAILED")

if __name__ == "__main__":
    main() 