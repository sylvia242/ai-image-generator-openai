#!/usr/bin/env python3
"""
Real Products Pathway - AI Image Generator (BACKUP)
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
    
    def multi_image_edit(self, base_image_path: str, product_images: List[str], products: List[Dict]) -> str:
        """Use GPT Image 1's multi-image capability to send base + all product images together"""
        
        try:
            # Create product descriptions for the prompt
            product_descriptions = []
            for i, product in enumerate(products, 1):
                area = product.get('area', 'General')
                name = product.get('name', 'Unknown Product')
                price = product.get('price')
                retailer = product.get('retailer', 'Online Store')
                
                price_info = f" (${price})" if price else ""
                product_descriptions.append(f"{i}. {name} - {area} - {retailer}{price_info}")
            
            # Create comprehensive prompt
            prompt = create_real_products_pathway_prompt(products)
            
            print("🔧 Preparing multi-image request for GPT Image 1...")
            
            # Prepare the API request
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Prepare files dictionary with base image and all product images
            files = {
                'image': (base_image_path, open(base_image_path, 'rb'), 'image/png'),
                'prompt': (None, prompt),
                'n': (None, '1'),
                'size': (None, '1024x1024'),
                'model': (None, 'gpt-image-1')
            }
            
            # Add each product image with a unique key
            for i, product_path in enumerate(product_images):
                if os.path.exists(product_path):
                    files[f'image{i+2}'] = (product_path, open(product_path, 'rb'), 'image/png')
                    print(f"   📸 Added product image {i+1}: {os.path.basename(product_path)}")
            
            # Make API call
            response = requests.post(
                self.image_edit_url,
                headers=headers,
                files=files,
                timeout=120
            )
            
            # Close all file handles
            for key, file_data in files.items():
                if key.startswith('image') and len(file_data) >= 2:
                    file_handle = file_data[1]
                    if hasattr(file_handle, 'close'):
                        file_handle.close()
            
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
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    final_filename = f"multi_image_real_products_design_{timestamp}.png"
                    
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
            raise Exception(f"Error in multi-image real products editing: {str(e)}")
    
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
                                image_url, real_product['name']
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
            
            # Step 4: Generate final design using multi-image approach
            print("🎨 Step 4: Generating final design with real products (multi-image approach)...")
            
            # Get product image paths
            product_image_paths = [p['permanent_image_path'] for p in real_products_with_images]
            
            # Call GPT Image 1 API with base image + all product images
            response = self.multi_image_edit(image_path, product_image_paths, real_products_with_images)
            
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
            
            # Compile final results
            analysis_results['serpapiProductsComposition'] = {
                'method': 'multi_image_real_products',
                'products_used': len(real_products_with_images),
                'products_info': real_products_with_images,
                'final_image': {
                    'filename': final_filename,
                    'method': 'gpt_image_1_multi_image'
                }
            }
            
            return analysis_results
            
        except Exception as e:
            raise Exception(f"Error in SerpAPI Google Shopping products design generation: {str(e)}") 