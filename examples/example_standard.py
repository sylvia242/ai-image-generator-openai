#!/usr/bin/env python3
"""
Example usage of the AI Image Generator - Standard Pathway
This script demonstrates the standard pathway: analysis + AI-imagined products
"""

import os
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.ai_image_generator import AIImageGenerator
from config.config_settings import get_api_key

def main():
    # Get OpenAI API key from config
    api_key = get_api_key()
    
    if not api_key:
        print("❌ Error: Please set your OpenAI API key via:")
        print("   1. Environment variable: export OPENAI_API_KEY='your_key'")
        print("   2. Edit config.py and set the API_KEY variable")
        print("   3. Create a .env file with: OPENAI_API_KEY=your_key")
        return
    
    # Initialize the generator
    generator = AIImageGenerator(api_key)
    
    # Example image path (replace with your actual image)
    image_path = "sample_room.jpg"  # Replace with your image file
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"❌ Please add an image file named '{image_path}' to test the script")
        print("   You can use any JPG, PNG, GIF, or WebP image file")
        return
    
    try:
        print("🚀 Starting Standard Pathway - AI Interior Design Pipeline...")
        print("   📋 Step 1: GPT-4o will analyze your image")
        print("   🎨 Step 2: GPT Image 1 will generate AI-imagined products")
        print("   💾 Step 3: Download and save the new design")
        
        # Generate complete design with image generation
        results = generator.generate_design(
            image_path=image_path,
            design_style="modern scandinavian",
            custom_instructions="Focus on natural materials, warm lighting, and cozy atmosphere. Add plants and improve the flow of the space.",
            design_type="living room redesign",
            generate_image=True  # This enables image generation
        )
        
        # Display results
        generator.print_results(results)
        
        # Save results
        generator.save_results(results, "example_results.json")
        
        print("\n" + "="*60)
        print("✅ STANDARD PATHWAY SUCCESS!")
        print("="*60)
        print("📊 Analysis saved to: example_results.json")
        
        if 'generatedImage' in results:
            img_info = results['generatedImage']
            print(f"🖼️  Redesigned image: {img_info['filename']}")
            print(f"🔗 Original GPT Image 1 URL: {img_info['url']}")
            print("\n💡 You now have:")
            print("   • Detailed AI analysis of your original image")
            print("   • Professional design recommendations")
            print("   • A brand new redesigned image with AI-imagined products")
        
        print("\n🎨 Try different styles by running:")
        print("   python3 ai_image_generator.py your_image.jpg --style 'minimalist'")
        print("   python3 ai_image_generator.py your_image.jpg --style 'rustic farmhouse'")
        print("   python3 ai_image_generator.py your_image.jpg --analysis-only  # Skip image generation")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n💡 Troubleshooting tips:")
        print("   • Make sure your OpenAI API key is valid and has credits")
        print("   • Check that your image file exists and is readable")
        print("   • Ensure you have internet connection for API calls")
        print("   • GPT Image 1 generation can take 30-60 seconds, please be patient")

if __name__ == "__main__":
    main() 