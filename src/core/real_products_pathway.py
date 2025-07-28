#!/usr/bin/env python3
"""
Real Products Pathway - AI Image Generator
Handles real product images pathway using multi-image approach
"""

import os
import base64
import json
import requests
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime
from .prompts import create_analysis_prompt, create_real_products_pathway_prompt
from src.shopping.serpapi_shopping_integration import SerpAPIShopping


class RealProductsPathway:
    """Handles the real products pathway: actual product images"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.vision_model = "gpt-4o"
        self.chat_url = "https://api.openai.com/v1/chat/completions"
        self.image_edit_url = "https://api.openai.com/v1/images/edits"
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64 for API submission"""
        try:
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
            extension = Path(image_path).suffix.lower()
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
                "max_tokens": 2048,
                "temperature": 0.7
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
    
    def create_composite_layout(self, base_image_path: str, product_images: List[str], products: List[Dict], output_dir: str) -> str:
        """Create a side-by-side composite image with base image on left and products on right"""
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            print("🔧 Creating composite layout with base image and products...")
            
            # Use the output directory passed from the main function
            # The output_dir is now created in the main function and passed here
            
            # Load base image
            base_img = Image.open(base_image_path)
            base_width, base_height = base_img.size
            
            # Calculate layout dimensions
            # We'll create a layout that's 2x the base width to accommodate side-by-side
            composite_width = base_width * 2
            composite_height = base_height
            
            # Create composite canvas
            composite = Image.new('RGB', (composite_width, composite_height), 'white')
            
            # Place base image on the left side
            composite.paste(base_img, (0, 0))
            
            # Create product grid on the right side
            right_side_x = base_width
            right_side_width = base_width
            
            # Calculate grid layout for products
            num_products = len(product_images)
            if num_products <= 4:
                grid_cols = 2
                grid_rows = 2
            elif num_products <= 6:
                grid_cols = 3
                grid_rows = 2
            else:
                grid_cols = 4
                grid_rows = 3
            
            # Calculate cell dimensions
            cell_width = right_side_width // grid_cols
            cell_height = composite_height // grid_rows
            
            # Add products to the grid
            for i, (product_path, product_info) in enumerate(zip(product_images, products)):
                if i >= grid_cols * grid_rows:  # Limit to grid capacity
                    break
                    
                if os.path.exists(product_path):
                    try:
                        # Load and resize product image
                        product_img = Image.open(product_path)
                        product_img = product_img.resize((cell_width - 10, cell_height - 10), Image.Resampling.LANCZOS)
                        
                        # Calculate position in grid
                        row = i // grid_cols
                        col = i % grid_cols
                        x = right_side_x + (col * cell_width) + 5
                        y = (row * cell_height) + 5
                        
                        # Paste product image
                        composite.paste(product_img, (x, y))
                        
                        # Add product label
                        draw = ImageDraw.Draw(composite)
                        try:
                            # Try to use a default font
                            font = ImageFont.load_default()
                        except:
                            font = None
                        
                        # Add product name as label
                        product_name = product_info.get('name', f'Product {i+1}')
                        label_text = f"{i+1}. {product_name[:20]}..."
                        
                        # Draw label background
                        text_bbox = draw.textbbox((0, 0), label_text, font=font)
                        text_width = text_bbox[2] - text_bbox[0]
                        text_height = text_bbox[3] - text_bbox[1]
                        
                        label_x = x + (cell_width - text_width) // 2
                        label_y = y + cell_height - text_height - 5
                        
                        # Draw background rectangle
                        draw.rectangle([
                            label_x - 2, label_y - 2,
                            label_x + text_width + 2, label_y + text_height + 2
                        ], fill='black', outline='white')
                        
                        # Draw text
                        draw.text((label_x, label_y), label_text, fill='white', font=font)
                        
                        print(f"   📸 Added product {i+1}: {os.path.basename(product_path)}")
                        
                    except Exception as e:
                        print(f"   ⚠️  Failed to add product {i+1}: {str(e)}")
                        continue
            
            # Save composite image in the organized directory
            composite_filename = os.path.join(output_dir, "composite_layout.png")
            composite.save(composite_filename, 'PNG')
            
            print(f"✅ Composite layout created: {composite_filename}")
            return composite_filename
            
        except Exception as e:
            raise Exception(f"Error creating composite layout: {str(e)}")
    
    def overlay_products_with_gpt_image_1(self, composite_image_path: str, products: List[Dict]) -> str:
        """Use GPT Image 1 to overlay products from composite layout onto base image"""
        
        try:
            # Create detailed product descriptions for the prompt
            product_details = []
            for i, product in enumerate(products, 1):
                area = product.get('area', 'General')
                name = product.get('name', 'Unknown Product')
                price = product.get('price')
                retailer = product.get('retailer', 'Online Store')
                
                price_info = f" (${price})" if price else ""
                product_details.append(f"{i}. {name} - {area} - {retailer}{price_info}")
            
            # Create comprehensive prompt for GPT Image 1
            prompt = f"""Transform this interior design by adding these real products naturally into the room.

You can see the base room image on the left side and the product images on the right side of this composite image.

REAL PRODUCTS TO ADD:
{chr(10).join(product_details)}

CRITICAL INSTRUCTIONS:
- Look at the base room image (left side) and the product images (right side)
- Add each product naturally to the appropriate area of the room
- Maintain the original room structure, lighting, and perspective
- Place products in realistic, functional positions
- Keep the overall design cohesive and professional
- Use the exact products shown in the reference images - do not substitute with different items
- Ensure each product is clearly visible and properly integrated
- Maintain the modern minimalist aesthetic of the room
- Make the final result look professional and polished
- Try to preserve existing elements where possible, but prioritize natural product integration"""
            
            print("🔧 Preparing GPT Image 1 overlay request...")
            print(f"   📸 Using composite layout with {len(products)} products")
            
            # Prepare the API request
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Prepare files dictionary with composite image
            files = {
                'image': (composite_image_path, open(composite_image_path, 'rb'), 'image/png'),
                'prompt': (None, prompt),
                'n': (None, '1'),
                'size': (None, '1024x1024'),
                'model': (None, 'gpt-image-1')
            }
            
            # Make API call
            response = requests.post(
                self.image_edit_url,
                headers=headers,
                files=files,
                timeout=120
            )
            
            # Close file handle
            files['image'][1].close()
            
            if not response.ok:
                error_details = response.text
                raise Exception(f"OpenAI Image Edit API Error: {response.status_code} - {error_details}")
            
            result = response.json()
            print(f"🔍 API Response keys: {list(result.keys())}")
            
            # Extract image URL
            if 'data' in result and len(result['data']) > 0:
                image_data = result['data'][0]
                print(f"🔍 Image data keys: {list(image_data.keys())}")
                
                if 'url' in image_data:
                    image_url = image_data['url']
                    return image_url
                elif 'b64_json' in image_data:
                    # Handle base64 encoded image
                    b64_data = image_data['b64_json']
                    
                    # Decode base64 and save directly
                    # Extract directory from composite image path
                    composite_dir = os.path.dirname(composite_image_path)
                    final_filename = os.path.join(composite_dir, "real_products_overlay_design.png")
                    
                    try:
                        import base64
                        image_bytes = base64.b64decode(b64_data)
                        with open(final_filename, 'wb') as f:
                            f.write(image_bytes)
                        return final_filename
                    except Exception as decode_error:
                        raise Exception(f"Failed to decode base64 image: {str(decode_error)}")
                else:
                    raise Exception(f"No 'url' or 'b64_json' key in image data. Available keys: {list(image_data.keys())}")
            else:
                raise Exception(f"No image data returned from API. Response: {result}")
                
        except Exception as e:
            raise Exception(f"Error in GPT Image 1 overlay: {str(e)}")
    
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
                                         serpapi_key: str = None) -> Dict[str, Any]:
        """Complete real products pathway design generation: analyze + search + multi-image integration"""
        
        try:
            print("🔍 Step 1: Analyzing original image with GPT-4o Vision...")
            
            # Step 1: Analyze the original image
            analysis_results = self.analyze_image(
                image_path=image_path,
                design_style=design_style,
                custom_instructions=custom_instructions,
                design_type=design_type
            )
            
            print("🛒 Step 2: Searching for real products using SerpAPI Google Shopping...")
            
            # Step 2: Initialize SerpAPI Google Shopping
            serpapi_shopping = SerpAPIShopping(serpapi_key)
            
            # Extract recommendations and color palette
            recommendations = analysis_results.get('recommendations', [])
            color_palette = analysis_results.get('colorPalette', {}).get('primary', [])
            
            # Step 3: Search for real products using SerpAPI Google Shopping
            print("🛒 Step 3: Searching for real products using SerpAPI Google Shopping...")
            
            real_products_with_images = []
            temp_image_files = []
            
            for product in recommendations:
                print(f"   🔍 Searching Google Shopping for: {product['type']}")
                
                # Search for real products using SerpAPI Google Shopping
                search_results = serpapi_shopping.search_interior_products(
                    product_type=product['type'],
                    style=design_style,
                    colors=color_palette
                )
                
                if search_results:
                    # Take the first product with an image
                    for real_product in search_results:
                        image_url = real_product.get('image')
                        if image_url:
                            # Download the product image
                            local_image_path = serpapi_shopping.download_product_image(
                                image_url, real_product['name'], output_dir
                            )
                            
                            if local_image_path:
                                # Update product info with local image path and ensure URL is stored
                                real_product['permanent_image_path'] = local_image_path
                                real_product['area'] = product['area']
                                real_product['product_url'] = real_product.get('url', '')  # Ensure URL is stored
                                real_products_with_images.append(real_product)
                                print(f"   ✅ Found product with image: {real_product['name']}...")
                                break  # Only use one product per type
                            else:
                                print(f"   ❌ No image found for: {real_product['name']}")
                        else:
                            print(f"   ❌ No image available for: {real_product['name']}")
                else:
                    print(f"   ❌ No products found for: {product['type']}")
            
            if not real_products_with_images:
                raise ValueError("No real products with images found for design composition")
            
            print(f"   🎉 Found {len(real_products_with_images)} products with images")
            
            # Limit to 15 products maximum for better performance
            if len(real_products_with_images) > 15:
                print(f"   ⚠️  Limiting to first 15 products (found {len(real_products_with_images)})")
                real_products_with_images = real_products_with_images[:15]
            
            # Step 4: Create composite layout with base image and products
            print("🎨 Step 4: Creating composite layout with base image and products...")
            
            # Create output directory based on input image name
            base_image_name = os.path.splitext(os.path.basename(image_path))[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = f"serpapi_products/{base_image_name}_{timestamp}"
            os.makedirs(output_dir, exist_ok=True)
            
            # Get product image paths
            product_image_paths = [p['permanent_image_path'] for p in real_products_with_images]
            
            # Create composite layout (base image on left, products on right)
            composite_image_path = self.create_composite_layout(image_path, product_image_paths, real_products_with_images, output_dir)
            
            # Step 5: Use GPT Image 1 to overlay products onto base image
            print("🎨 Step 5: Using GPT Image 1 to overlay products onto base image...")
            
            # Call GPT Image 1 API with composite image
            response = self.overlay_products_with_gpt_image_1(composite_image_path, real_products_with_images)
            
            if not response:
                raise ValueError("Failed to generate design with real products")
            
            # Handle response (could be URL or local filename)
            if isinstance(response, str):
                if response.startswith('http'):
                    # It's a URL, download it
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    final_filename = f"serpapi_products_design_{timestamp}.png"
                    self.download_image(response, final_filename)
                else:
                    # It's already a local filename
                    final_filename = response
            else:
                raise ValueError("Unexpected response format from GPT Image 1 API")
            
            # Clean up temporary files
            for temp_file in temp_image_files:
                try:
                    os.remove(temp_file)
                except:
                    pass
            
            # Add real products composition info to results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            analysis_results['serpapiProductsComposition'] = {
                'method': 'composite_layout_overlay',
                'products_used': len(real_products_with_images),
                'composite_layout': composite_image_path,
                'products_info': [
                    {
                        'name': p['name'],
                        'area': p['area'],
                        'product_url': p.get('url', ''),  # Use the actual URL from SerpAPI
                        'price': p.get('price'),
                        'retailer': p.get('retailer'),
                        'rating': p.get('rating'),
                        'reviews': p.get('reviews'),
                        'permanent_image_path': p.get('permanent_image_path', '')
                    } for p in real_products_with_images
                ],
                'final_image': {
                    'localPath': final_filename,
                    'filename': final_filename,
                    'generatedAt': timestamp,
                    'method': 'gpt_image_1_composite_overlay'
                },
                'overlay_approach': {
                    'method': 'composite_layout_overlay',
                    'description': 'Base image + products in composite layout, then GPT Image 1 overlay'
                }
            }
            
            # Save to JSON file
            with open('design_results.json', 'w') as f:
                json.dump(analysis_results, f, indent=2)
            
            print(f"✅ SerpAPI Google Shopping products design saved as: {final_filename}")
            print(f"📊 Used {len(real_products_with_images)} real products from SerpAPI Google Shopping")
            
            return analysis_results
            
        except Exception as e:
            print(f"❌ Error in SerpAPI Google Shopping products design generation: {e}")
            return None 