#!/usr/bin/env python3
"""
Test script to debug image generation from composite layout
Uses the standard mode composite image to test GPT Image 1 generation
"""

import os
import sys
import openai
import requests
from datetime import datetime
from PIL import Image

# Add src to path
sys.path.append('src')

from src.core.real_products_pathway import RealProductsPathway

def test_image_generation_from_composite():
    """Test image generation using the standard mode composite image"""
    
    # Set up API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set OPENAI_API_KEY environment variable")
    
    # Initialize the pathway
    pathway = RealProductsPathway(api_key=api_key, fast_mode=False)  # Use full quality for debugging
    
    # Use the standard mode composite image
    composite_image_path = "serpapi_products/Screenshot 2025-07-29 at 7.36.09 PM_20250731_205456/composite_layout_20250731_205540.png"
    
    if not os.path.exists(composite_image_path):
        print(f"❌ Composite image not found: {composite_image_path}")
        return
    
    print(f"🔍 Testing image generation from composite: {composite_image_path}")
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"debug_output_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Test the overlay function directly
        print("🎨 Step 1: Testing GPT Image 1 overlay...")
        
        # Create the prompt for GPT Image 1
        prompt = """You are an expert interior designer. 
I have provided you with a composite image showing an existing room on the left side and product images to overlay into the room on the right side. 

The products on the right are organized by type (e.g., multiple throw pillows, multiple lamps, etc.). 
Each row on the right side is a different product type.

Your task is to intelligently select and integrate the best combination of products into the existing room.
You should not alter the existing room conditions - 
specifically keep the existing walls where they are, don't change room dimensions or furniture as long as you don't want to replace it.  
Your only goal is to overlay the products into the room in a way that looks like a professional interior design photo.

PRODUCT SELECTION STRATEGY:
- Analyze all product options for each category
- Select products that will work well together and enhance the room
- Choose products that complement each other in style, color, and scale
- Avoid overwhelming the space - select a balanced combination
- Consider the existing room elements and choose products that enhance them
- If multiple products of the same type exist, pick the one that best fits the room's style and color scheme
- You have complete freedom to choose which products to include - focus on what works best for the room

INTEGRATION REQUIREMENTS:
- Place selected products naturally and realistically in the room
- Maintain the original room's lighting, perspective, and style
- Ensure products look like they belong in the space
- Create a cohesive, professional interior design
- Preserve the room's existing architecture and layout
- Make the final design look like a professional interior photography
- Work with existing elements - if the room already has suitable items, integrate new products to complement rather than replace them

DESIGN PRINCIPLES:
- Less is more - don't overcrowd the space
- Choose products that create visual harmony
- Consider scale and proportion
- Ensure the final design feels intentional and curated
- The result should look like a professionally designed room with carefully selected products naturally integrated."""
        
        print("📝 Using prompt:")
        print("=" * 50)
        print(prompt)
        print("=" * 50)
        
        # Prepare the image for GPT Image 1 (Image Edit API)
        print("🖼️ Preparing image for GPT Image 1...")
        
        # Load and prepare the image
        img = Image.open(composite_image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to 1024x1024 (GPT Image 1 requirement)
        img = img.resize((1024, 1024), Image.Resampling.LANCZOS)
        
        # Save as PNG for GPT Image 1
        prepared_image_path = os.path.join(output_dir, "prepared_composite.png")
        img.save(prepared_image_path, 'PNG')
        
        print(f"✅ Prepared image saved as: {prepared_image_path}")
        
        # Use GPT Image 1 (Image Edit API)
        print("🖼️ Calling GPT Image 1 (Image Edit API)...")
        
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        with open(prepared_image_path, 'rb') as image_file:
            files = {
                'image': image_file,
                'prompt': (None, prompt),
                'n': (None, '1'),
                'size': (None, '1024x1024'),
                'model': (None, 'gpt-image-1'),
                'input_fidelity': (None, 'high')
            }
            
            response = requests.post(
                "https://api.openai.com/v1/images/edits",
                headers=headers,
                files=files,
                timeout=120
            )
        
        if not response.ok:
            error_details = response.text
            print(f"❌ GPT Image 1 Error: {response.status_code} - {error_details}")
            return
        
        result = response.json()
        print(f"✅ GPT Image 1 response received")
        print(f"🔍 Response keys: {list(result.keys())}")
        
        # Save the generated image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_image_path = os.path.join(output_dir, f"gpt_image_1_result_{timestamp}.png")
        
        # Extract image data from GPT Image 1 response
        if 'data' in result and len(result['data']) > 0:
            data_item = result['data'][0]
            
            # Check if we have URL or base64 data
            if 'url' in data_item:
                print(f"✅ GPT Image 1 edit successful (URL)")
                # Download and save the image
                image_response = requests.get(data_item['url'])
                image_response.raise_for_status()
                
                with open(final_image_path, 'wb') as f:
                    f.write(image_response.content)
            elif 'b64_json' in data_item:
                print(f"✅ GPT Image 1 edit successful (base64)")
                # Convert base64 to file
                import base64
                image_data = base64.b64decode(data_item['b64_json'])
                
                with open(final_image_path, 'wb') as f:
                    f.write(image_data)
            else:
                raise Exception("No image data found in GPT Image 1 response")
        else:
            raise Exception("No data in GPT Image 1 response")
        
        print(f"✅ GPT Image 1 result saved as: {final_image_path}")
        
        # Open the images
        print("\n🖼️ Opening generated images...")
        os.system(f"open '{final_image_path}'")
        os.system(f"open '{prepared_image_path}'")
        
        print(f"\n📁 All debug files saved in: {output_dir}")
        
    except Exception as e:
        print(f"❌ Error during GPT Image 1 generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_image_generation_from_composite() 