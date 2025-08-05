#!/usr/bin/env python3
"""
Real Products Pathway
Uses real product images from SerpAPI Google Shopping for AI design composition
"""

import os
import sys
import base64
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from PIL import Image
import openai
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.append('.')

from src.shopping.serpapi_shopping_integration import SerpAPIShopping
from .prompts import create_analysis_prompt, create_real_products_pathway_prompt
from performance_tracking.performance_tracker import create_tracker, track_vision_analysis, track_product_search, track_image_generation, track_composite_creation


class RealProductsPathway:
    """Handles the real products pathway: actual product images"""
    
    def __init__(self, api_key: str, fast_mode: bool = False):
        self.api_key = api_key
        # Use faster model in fast mode
        self.vision_model = "gpt-4o-mini" if fast_mode else "gpt-4o"
        self.fast_mode = fast_mode
        self.chat_url = "https://api.openai.com/v1/chat/completions"
        self.image_edit_url = "https://api.openai.com/v1/images/edits"
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64 for API submission"""
        try:
            # Optimize image size in fast mode
            if self.fast_mode:
                from PIL import Image
                with Image.open(image_path) as img:
                    # Resize to max 1024x1024 for faster processing
                    img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
                    
                    # Convert to RGB if necessary (JPEG doesn't support transparency)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        # Create white background for transparent images
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Save to memory as JPEG for smaller size
                    import io
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format='JPEG', quality=85, optimize=True)
                    img_buffer.seek(0)
                    image_data = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
                    return image_data
            else:
                # Original encoding for full quality
                with open(image_path, 'rb') as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')
                return image_data
        except Exception as e:
            raise Exception(f"Error encoding image: {str(e)}")
    
    def prepare_image_for_edit(self, image_path: str) -> str:
        """Prepare and resize image for OpenAI Edit API (must be PNG, square, <4MB)"""
        try:
            from PIL import Image
            
            # Open image
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to 1024x1024 (OpenAI requirement)
            img = img.resize((1024, 1024), Image.Resampling.LANCZOS)
            
            # Save as PNG
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            prepared_path = f"temp_prepared_{timestamp}.png"
            img.save(prepared_path, 'PNG')
            
            return prepared_path
            
        except Exception as e:
            raise Exception(f"Error preparing image: {str(e)}")
    
    def analyze_image(self, 
                     image_path: str, 
                     design_style: str = "modern",
                     custom_instructions: str = "",
                     design_type: str = "interior redesign") -> Dict[str, Any]:
        """Analyze image with GPT-4o Vision"""
        
        try:
            # Encode the image
            base64_image = self.encode_image(image_path)
            
            # Create the prompt
            prompt = create_analysis_prompt(design_style, custom_instructions, design_type)
            
            # Determine image MIME type
            extension = os.path.splitext(image_path)[1].lower()
            mime_types = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg', 
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }
            mime_type = mime_types.get(extension, 'image/jpeg')
            
            # Prepare the API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self.vision_model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                # Optimize for speed in fast mode
                "max_tokens": 2048 if self.fast_mode else 3072,
                "temperature": 0 if self.fast_mode else 0.7
            }
            
            # Make API call
            response = requests.post(
                self.chat_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if not response.ok:
                error_details = response.text
                raise Exception(f"OpenAI Vision API Error: {response.status_code} - {error_details}")
            
            result = response.json()
            
            # Extract and parse the response
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                
                # Try to extract JSON from the response
                try:
                    # Look for JSON block in the response
                    if "```json" in content:
                        json_start = content.find("```json") + 7
                        json_end = content.find("```", json_start)
                        json_content = content[json_start:json_end].strip()
                    elif content.strip().startswith('{'):
                        json_content = content.strip()
                    else:
                        # If no clear JSON structure, try to find the first { and last }
                        start_idx = content.find('{')
                        end_idx = content.rfind('}')
                        if start_idx != -1 and end_idx != -1:
                            json_content = content[start_idx:end_idx+1]
                        else:
                            raise Exception("No JSON found in response")
                    
                    design_data = json.loads(json_content)
                    return design_data
                    
                except json.JSONDecodeError as e:
                    print(f"⚠️  JSON parsing error: {e}")
                    print(f"Raw response: {content[:500]}...")
                    raise Exception(f"Failed to parse AI response as JSON: {e}")
                    
            else:
                raise Exception("No response from OpenAI Vision API")
                
        except Exception as e:
            raise Exception(f"Error in image analysis: {str(e)}")
    
    def create_composite_layout(self, base_image_path: str, products: List[Dict], output_dir: str) -> str:
        """Create a composite layout with base image on left and products on right, maintaining aspect ratios"""
        try:
            print("🔧 Creating composite layout with base image and products...")
            
            # Load base image
            base_img = Image.open(base_image_path)
            base_width, base_height = base_img.size
            base_aspect_ratio = base_width / base_height
            
            print(f"   📐 Original base image: {base_width}x{base_height} (aspect ratio: {base_aspect_ratio:.2f})")
            
            # Apply fast mode optimizations for composite layout
            if self.fast_mode:
                print("   ⚡ Using fast mode optimizations for composite layout")
                # Use medium-sized product thumbnails for better balance
                product_size = 150  # Middle ground between 100 and 200
                # Resize base image to medium size while maintaining aspect ratio
                max_base_size = 768  # Middle ground between 512 and 1024
                if base_width > max_base_size or base_height > max_base_size:
                    # Calculate new dimensions maintaining aspect ratio
                    if base_aspect_ratio > 1:  # Landscape
                        new_width = max_base_size
                        new_height = int(max_base_size / base_aspect_ratio)
                    else:  # Portrait
                        new_height = max_base_size
                        new_width = int(max_base_size * base_aspect_ratio)
                    
                    base_img = base_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    base_width, base_height = base_img.size
                    print(f"   📏 Resized base image to {base_width}x{base_height} for fast mode (maintaining aspect ratio)")
            else:
                product_size = 200  # Standard size
                # Resize base image if it's too large while maintaining aspect ratio
                if base_width > 1024 or base_height > 1024:
                    # Calculate new dimensions maintaining aspect ratio
                    if base_aspect_ratio > 1:  # Landscape
                        new_width = 1024
                        new_height = int(1024 / base_aspect_ratio)
                    else:  # Portrait
                        new_height = 1024
                        new_width = int(1024 * base_aspect_ratio)
                    
                    base_img = base_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    base_width, base_height = base_img.size
                    print(f"   📏 Resized base image to {base_width}x{base_height} (maintaining aspect ratio)")
            
            # Calculate layout dimensions
            products_per_row = 3
            num_products = len(products)
            num_rows = (num_products + products_per_row - 1) // products_per_row
            
            # Calculate composite dimensions - ensure base image maintains its aspect ratio
            products_area_width = product_size * products_per_row
            products_area_height = product_size * num_rows
            
            # The composite height should accommodate both base image and products properly
            composite_width = base_width + products_area_width
            composite_height = max(base_height, products_area_height)
            
            print(f"   📐 Composite dimensions: {composite_width}x{composite_height}")
            print(f"   📐 Base image area: {base_width}x{base_height} (aspect ratio: {base_width/base_height:.2f})")
            print(f"   📐 Products area: {products_area_width}x{products_area_height}")
            
            # Create composite image
            composite = Image.new('RGB', (composite_width, composite_height), 'white')
            
            # Center the base image vertically if the composite is taller than the base image
            base_y_offset = max(0, (composite_height - base_height) // 2)
            composite.paste(base_img, (0, base_y_offset))
            print(f"   📐 Base image placed at: (0, {base_y_offset})")
            
            # Group products by type for better organization
            products_by_type = {}
            for product in products:
                product_type = product.get('product_type', 'unknown')
                if product_type not in products_by_type:
                    products_by_type[product_type] = []
                products_by_type[product_type].append(product)
            
            # Place products on the right, organized by type
            product_index = 0
            for product_type, type_products in products_by_type.items():
                print(f"   📦 Grouping {len(type_products)} {product_type} products")
                
                for product in type_products:
                    try:
                        # Load product image
                        product_img = Image.open(product['image_path'])
                        original_product_width, original_product_height = product_img.size
                        product_aspect_ratio = original_product_width / original_product_height
                        
                        # Resize product image while maintaining aspect ratio
                        if product_aspect_ratio > 1:  # Landscape
                            new_product_width = product_size
                            new_product_height = int(product_size / product_aspect_ratio)
                        else:  # Portrait or square
                            new_product_height = product_size
                            new_product_width = int(product_size * product_aspect_ratio)
                        
                        product_img = product_img.resize((new_product_width, new_product_height), Image.Resampling.LANCZOS)
                        
                        # Calculate position
                        row = product_index // products_per_row
                        col = product_index % products_per_row
                        x = base_width + (col * product_size)
                        y = row * product_size
                        
                        # Center the product image within its allocated space
                        x_offset = (product_size - new_product_width) // 2
                        y_offset = (product_size - new_product_height) // 2
                        x += x_offset
                        y += y_offset
                        
                        # Paste product image
                        composite.paste(product_img, (x, y))
                        
                        print(f"   📸 Added {product_type} product {product_index+1}: {os.path.basename(product['image_path'])} ({new_product_width}x{new_product_height})")
                        product_index += 1
                        
                    except Exception as e:
                        print(f"   ⚠️  Error adding product {product_index+1}: {e}")
                        product_index += 1
                        continue
            
            # Apply final fast mode optimization to composite while maintaining aspect ratio
            if self.fast_mode:
                # Resize entire composite to medium size for better quality
                max_composite_size = 1024  # Middle ground between 768 and unlimited
                composite_aspect_ratio = composite_width / composite_height
                
                if composite_width > max_composite_size or composite_height > max_composite_size:
                    # Calculate new dimensions maintaining aspect ratio
                    if composite_aspect_ratio > 1:  # Landscape
                        new_composite_width = max_composite_size
                        new_composite_height = int(max_composite_size / composite_aspect_ratio)
                    else:  # Portrait
                        new_composite_height = max_composite_size
                        new_composite_width = int(max_composite_size * composite_aspect_ratio)
                    
                    composite = composite.resize((new_composite_width, new_composite_height), Image.Resampling.LANCZOS)
                    print(f"   📏 Resized composite to {composite.width}x{composite.height} for fast mode (maintaining aspect ratio)")
            
            # Save composite
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            composite_path = os.path.join(output_dir, f"composite_layout_{timestamp}.png")
            composite.save(composite_path)
            
            print(f"✅ Composite layout created: {composite_path}")
            return composite_path
            
        except Exception as e:
            print(f"❌ Error creating composite layout: {e}")
            raise
    
    def overlay_products_with_gpt_image_1(self, composite_image_path: str, output_dir: str) -> str:
        """Use GPT Image 1 to overlay products from composite onto base image"""
        try:
            print("🔧 Preparing GPT Image 1 overlay request...")
            
            # Create the prompt for GPT Image 1
            prompt = """Overlay the product images from the right side into the room on the left side.

Rules:
- Keep the original room (left part of image) EXACTLY as is. 
- Don't change dimensions, furniture, or camera position.
- Place products exactly as they appear in the product images. 
- Do NOT alter products: Do not change colors, shapes, or textures of products and original room
- Choose a few products - as many as you think look good together
- Place them in logical locations within the room"""
            
            # Apply fast mode optimizations for image generation
            if self.fast_mode:
                print("   ⚡ Using fast mode optimizations for image generation")
                input_fidelity = "low"  # Use low fidelity for faster processing
            else:
                input_fidelity = "high"  # Use high fidelity for better quality
            
            # Prepare the image for GPT Image 1 (Image Edit API)
            print("🖼️ Preparing image for GPT Image 1...")
            
            # Load and prepare the image
            img = Image.open(composite_image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to 1024x1024 (GPT Image 1 requirement) while maintaining aspect ratio
            original_width, original_height = img.size
            original_aspect_ratio = original_width / original_height
            
            print(f"   📐 Original composite: {original_width}x{original_height} (aspect ratio: {original_aspect_ratio:.2f})")
            
            # Create a 1024x1024 canvas and center the image maintaining aspect ratio
            canvas = Image.new('RGB', (1024, 1024), 'white')
            
            # Calculate new dimensions to fit within 1024x1024 while maintaining aspect ratio
            if original_aspect_ratio > 1:  # Landscape
                new_width = 1024
                new_height = int(1024 / original_aspect_ratio)
            else:  # Portrait or square
                new_height = 1024
                new_width = int(1024 * original_aspect_ratio)
            
            # Resize the image maintaining aspect ratio
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Center the resized image on the canvas
            x_offset = (1024 - new_width) // 2
            y_offset = (1024 - new_height) // 2
            canvas.paste(img_resized, (x_offset, y_offset))
            
            print(f"   📐 Resized to: {new_width}x{new_height}, centered at ({x_offset}, {y_offset})")
            
            img = canvas
            
            # Save as PNG for GPT Image 1
            prepared_image_path = os.path.join(output_dir, "prepared_composite.png")
            img.save(prepared_image_path, 'PNG')
            
            print(f"✅ Prepared image saved as: {prepared_image_path}")
            
            # Use GPT Image 1 (Image Edit API)
            print("🖼️ Calling GPT Image 1 (Image Edit API)...")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            with open(prepared_image_path, 'rb') as image_file:
                files = {
                    'image': image_file,
                    'prompt': (None, prompt),
                    'n': (None, '1'),
                    'size': (None, '1024x1024'),
                    'model': (None, 'gpt-image-1'),
                    'input_fidelity': (None, input_fidelity)
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
                raise Exception(f"GPT Image 1 API Error: {response.status_code} - {error_details}")
            
            result = response.json()
            print(f"✅ GPT Image 1 response received")
            print(f"🔍 Response keys: {list(result.keys())}")
            
            # Save the generated image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            final_image_path = os.path.join(output_dir, f"real_products_overlay_design_{timestamp}.png")
            
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
            
            print(f"✅ SerpAPI Google Shopping products design saved as: {final_image_path}")
            return final_image_path
            
        except Exception as e:
            print(f"❌ Error in GPT Image 1 overlay: {e}")
            raise
    
    def download_image(self, image_url: str, output_path: str) -> str:
        """Download image from URL and save to local path"""
        try:
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Downloaded image to: {output_path}")
            return output_path
            
        except Exception as e:
            raise Exception(f"Error downloading image: {str(e)}")
    
    def generate_design_with_real_products(self, 
                                         image_path: str, 
                                         design_style: str = "modern",
                                         custom_instructions: str = "",
                                         design_type: str = "interior redesign",
                                         serpapi_key: str = None,
                                         fast_mode: bool = False) -> Dict[str, Any]:
        """Complete real products pathway design generation: analyze + search + multi-image integration"""
        
        # Initialize performance tracker
        tracker = create_tracker()
        tracker.start_pipeline(fast_mode=fast_mode)
        
        try:
            # Initialize SessionManager for organized file output
            from src.utils.session_manager import SessionManager
            session = SessionManager()
            print(f"📁 Session ID: {session.session_id}")
            
            # Save analysis results to session
            session.save_file('analysis', 'design_results.json', content=json.dumps({"status": "starting"}))
            
            print(f"📁 Using organized session: {session.session_path}")
            
            print("🔍 Step 1: Analyzing original image with GPT-4o Vision...")
            
            # Step 1: Analyze the original image with performance tracking
            analysis_results = None
            with track_vision_analysis(tracker, {
                "design_style": design_style,
                "design_type": design_type,
                "custom_instructions": custom_instructions
            }):
                analysis_results = self.analyze_image(
                    image_path=image_path,
                    design_style=design_style,
                    custom_instructions=custom_instructions,
                    design_type=design_type
                )
            
            if not analysis_results:
                tracker.end_pipeline(success=False, product_count=0)
                return {"error": "Failed to analyze image"}
            
            # Save analysis results to session
            session.save_file('analysis', 'analysis_results.json', content=json.dumps(analysis_results, indent=2))
            
            print("🛒 Step 2: Searching for real products using SerpAPI Google Shopping...")
            
            # Extract room analysis data for enhanced search
            room_analysis = analysis_results.get('roomAnalysis', {})
            if room_analysis:
                print(f"   📊 Room Analysis: {room_analysis.get('roomType', 'Unknown room type')}")
                print(f"   🎨 Mood: {room_analysis.get('mood', 'Unknown mood')}")
                print(f"   🏠 Style Details: {', '.join(room_analysis.get('styleDetails', []))}")
            
            # Initialize SerpAPI shopping
            serpapi_shopping = SerpAPIShopping(serpapi_key)
            
            # Extract recommendations and color palette
            recommendations = analysis_results.get('recommendations', [])
            color_palette = analysis_results.get('colorPalette', {}).get('primary', [])
            
            # Apply fast mode optimizations
            if fast_mode:
                print("   ⚡ Fast mode enabled - using aggressive optimizations")
                # Limit to top 3 product types in fast mode
                if len(recommendations) > 3:
                    recommendations = recommendations[:3]
                    print(f"   ⚡ Fast mode: Limited to top 3 product types")
            else:
                # Standard mode: search for up to 12 product types
                if len(recommendations) > 12:
                    recommendations = recommendations[:12]
                    print(f"   📦 Standard mode: Limited to top 12 product types")
            
            # Step 3: Search for real products using SerpAPI Google Shopping (PARALLEL)
            print("🛒 Step 3: Searching for real products using SerpAPI Google Shopping (PARALLEL)...")
            
            # Store session for parallel processing
            self.session = session
            
            # Calculate target products based on 70% of (product types × 3 alternatives)
            alternatives_per_type = 3
            target_products = int(len(recommendations) * alternatives_per_type * 0.7)
            early_exit_threshold = max(target_products, 3)  # Minimum of 3 products
            
            print(f"   🎯 Target: {len(recommendations)} types × {alternatives_per_type} alternatives = {len(recommendations) * alternatives_per_type} max")
            print(f"   ⚡ Early exit at 70%: {early_exit_threshold} products")
            
            # Use parallel search with performance tracking
            real_products_with_images = []
            with track_product_search(tracker, {
                "recommendations_count": len(recommendations),
                "design_style": design_style,
                "fast_mode": fast_mode,
                "target_products": target_products,
                "early_exit_threshold": early_exit_threshold
            }):
                real_products_with_images = self.search_products_parallel(
                    serpapi_shopping=serpapi_shopping,
                    recommendations=recommendations,
                    design_style=design_style,
                    color_palette=color_palette,
                    room_analysis=room_analysis,
                    early_exit_threshold=early_exit_threshold,
                    fast_mode=fast_mode
                )
            
            if not real_products_with_images:
                tracker.end_pipeline(success=False, product_count=0)
                raise ValueError("No real products with images found for design composition")
            
            print(f"   🎉 Found {len(real_products_with_images)} products with images")
            
            # Step 4: Create composite layout with base image and products
            print("🎨 Step 4: Creating composite layout with base image and products...")
            
            # Prepare products info for immediate return (before image generation)
            products_info = []
            for i, product in enumerate(real_products_with_images, 1):
                product_info = {
                    'name': product['name'],
                    'price': product['price'],
                    'retailer': product['retailer'],
                    'url': product['url'],
                    'rating': product.get('rating'),
                    'reviews': product.get('reviews'),
                    'image_path': product['image_path']
                }
                products_info.append(product_info)
            
            # Create composite layout with performance tracking
            composite_path = None
            with track_composite_creation(tracker, {
                "product_count": len(real_products_with_images),
                "fast_mode": fast_mode
            }):
                composite_path = self.create_composite_layout(image_path, real_products_with_images, session.get_path('composites'))
            
            # Step 5: Use GPT Image 1 to overlay products onto base image
            print("🎨 Step 5: Using GPT Image 1 to overlay products onto base image...")
            
            final_image_path = None
            with track_image_generation(tracker, {
                "fast_mode": fast_mode,
                "product_count": len(real_products_with_images)
            }):
                final_image_path = self.overlay_products_with_gpt_image_1(composite_path, session.get_path('final_designs'))
            
            # End performance tracking
            tracker.end_pipeline(success=True, product_count=len(real_products_with_images))
            
            # Save performance report to session
            report_path = tracker.save_performance_report()
            session.save_file('debug', 'performance_report.json', source_path=report_path)
            
            # Print performance summary
            tracker.print_summary()
            
            # Create latest symlink for easy access
            session.create_latest_symlink()
            
            # Debug: Log the final product data structure
            print(f"🔍 Final products_info structure:")
            for i, product in enumerate(real_products_with_images):
                print(f"   Product {i+1}: {product.get('name', 'Unknown')}")
                print(f"      URL: {product.get('url', 'No URL')}")
                print(f"      Image: {product.get('image_path', 'No image')}")
                print(f"      Price: {product.get('price', 'No price')}")
            
            return {
                'success': True,
                'session_id': session.session_id,
                'session_path': session.session_path,
                'original_image': image_path,
                'final_design': final_image_path,
                'products_info': products_info,
                'products_used': len(real_products_with_images),
                'design_style': design_style,
                'analysis_results': analysis_results,
                'performance_report': report_path,
                'total_duration': tracker.get_total_duration(),
                'step_durations': {
                    step.step_name: step.duration for step in tracker.steps
                }
            }
            
        except Exception as e:
            print(f"❌ Error in SerpAPI Google Shopping products design generation: {e}")
            tracker.end_pipeline(success=False, product_count=0)
            return {"error": str(e)} 

    def search_products_parallel(self, serpapi_shopping: SerpAPIShopping, recommendations: List[Dict], 
                                design_style: str, color_palette: List[str], room_analysis: Dict,
                                early_exit_threshold: int = 25, fast_mode: bool = False) -> List[Dict]:
        """Search for products in parallel using ThreadPoolExecutor with optimized HTTP connections
        
        Args:
            early_exit_threshold: Stop searching when we reach this many products (70% of target)
        """
        
        def search_single_product(product: Dict) -> List[Dict]:
            """Search for a single product type with optimized HTTP session"""
            try:
                print(f"   🔍 Searching Google Shopping for: {product['type']}")
                
                # Use enhanced search with variation for better results
                search_results = serpapi_shopping.search_interior_products_with_variation(
                    product_type=product['type'],
                    style=design_style,
                    colors=color_palette,
                    room_analysis=room_analysis,
                    max_results=10,
                    price_range=None,
                    sort_by="popularity"
                )
                
                if search_results and len(search_results) > 0:
                    # Download product images in parallel for this product type
                    products_with_images = []
                    for result in search_results[:3]:  # Limit to top 3 per product type
                        try:
                            image_path = serpapi_shopping.download_product_image(result)
                            if image_path:
                                # Save to session products directory
                                session = getattr(self, 'session', None)
                                if session:
                                    product_filename = f"{product['type']}_{os.path.basename(image_path)}"
                                    session_image_path = session.save_file('products', product_filename, source_path=image_path)
                                    result['image_path'] = session_image_path
                                else:
                                    result['image_path'] = image_path
                                result['product_type'] = product['type']  # Add product type for context
                                products_with_images.append(result)
                                print(f"   📸 Downloaded: {os.path.basename(image_path)}")
                        except Exception as e:
                            print(f"   ⚠️ Failed to download image for {result.get('name', 'Unknown')}: {e}")
                    
                    return products_with_images
                else:
                    print(f"   ❌ No results found for: {product['type']}")
                    return []
                    
            except Exception as e:
                print(f"   ❌ Error searching for {product['type']}: {e}")
                return []
        
        print(f"🚀 Starting parallel product search with up to 8 workers...")
        
        # Use up to 8 workers for better performance
        max_workers = min(len(recommendations), 8)
        print(f"   ⚡ Using {max_workers} parallel workers")
        
        real_products_with_images = []
        
        # Execute searches in parallel with optimized connection pooling
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all search tasks
            future_to_product = {
                executor.submit(search_single_product, product): product 
                for product in recommendations
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_product):
                product = future_to_product[future]
                try:
                    results = future.result()
                    if results:
                        real_products_with_images.extend(results)
                        print(f"   ✅ Found {len(results)} products for: {product['type']}")
                        
                        # Early exit when we reach 70% threshold
                        if len(real_products_with_images) >= early_exit_threshold:
                            print(f"   ⚡ Early exit at 70% threshold: {len(real_products_with_images)}/{early_exit_threshold} products")
                            break
                    else:
                        print(f"   ⚠️ No products found for: {product['type']}")
                        
                except Exception as e:
                    print(f"   ❌ Error processing {product['type']}: {e}")
        
        print(f"🎉 Found {len(real_products_with_images)} products with images")
        return real_products_with_images 