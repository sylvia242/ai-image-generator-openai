#!/usr/bin/env python3
"""
Standard Pathway - AI Image Generator
Handles AI-imagined products pathway
"""

import os
import base64
import json
import requests
from typing import Dict, Any
from pathlib import Path
from datetime import datetime
from .prompts import create_analysis_prompt, create_standard_pathway_prompt


class StandardPathway:
    """Handles the standard pathway: AI-imagined products"""
    
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
    
    def generate_variation(self, image_path: str, analysis_results: Dict[str, Any]) -> str:
        """Generate AI-imagined product variation using GPT Image 1"""
        
        try:
            # Extract key information from analysis
            recommendations = analysis_results.get('recommendations', [])
            color_palette = analysis_results.get('colorPalette', {}).get('primary', [])
            materials = analysis_results.get('materials', [])
            design_concept = analysis_results.get('designConcept', {})
            
            # Get style information
            style = design_concept.get('style', 'modern')
            style_instruction = f"Transform this room to {style} style"
            
            # Create comprehensive generation prompt
            generation_prompt = create_standard_pathway_prompt(analysis_results, style)
            
            # Include all recommendations for creative transformation
            all_recommendations = []
            
            # Prioritize by importance
            high_priority = [rec for rec in recommendations if rec.get('priority') == 'High']
            medium_priority = [rec for rec in recommendations if rec.get('priority') == 'Medium'] 
            low_priority = [rec for rec in recommendations if rec.get('priority') == 'Low']
            
            # Add all recommendations with clear implementation language
            for rec in high_priority:
                all_recommendations.append(f"• [HIGH PRIORITY] {rec.get('description', '')}")
            
            for rec in medium_priority:
                all_recommendations.append(f"• [MEDIUM] {rec.get('description', '')}")
                
            for rec in low_priority:
                all_recommendations.append(f"• [LOW] {rec.get('description', '')}")
            
            # Limit to top 6-8 recommendations for comprehensive transformation
            if len(all_recommendations) > 8:
                all_recommendations = all_recommendations[:8]
            
            # Add recommendations to prompt
            generation_prompt += "\n" + "\n".join(all_recommendations)
            
            # Add conservative styling requirements
            generation_prompt += f"""

TRANSFORMATION REQUIREMENTS:
- Implement ALL recommendations above with visible changes
- Use {', '.join(color_palette) if color_palette else 'appropriate'} color palette throughout the design
- Incorporate {', '.join(materials) if materials else 'quality'} materials for authenticity
- Allow furniture repositioning, replacement, and restyling as needed
- {style_instruction.capitalize()} through comprehensive design changes
- Maintain the same room layout and camera perspective
- Create a cohesive {style.lower()} aesthetic with professional interior design quality"""
            
            print(f"🎨 Generating new image with GPT-4o based on analysis...")
            print(f"🔥 Generation prompt: {generation_prompt[:200]}...")
            
            # Use OpenAI Image Edit API with GPT Image 1 for true image-to-image editing
            print(f"🖼️ Using OpenAI Image Edit API (GPT Image 1) for image-to-image transformation...")
            
            # Prepare the image for editing
            prepared_image_path = self.prepare_image_for_edit(image_path)
            
            # Create a comprehensive edit prompt (Image Edit API has character limits)
            if all_recommendations:
                # Get top 3 recommendations for the edit prompt
                top_changes = []
                for rec in all_recommendations[:3]:
                    if isinstance(rec, str):
                        # Clean up the priority tags and truncate
                        clean_rec = rec.replace('• [HIGH PRIORITY] ', '').replace('• [MEDIUM] ', '').replace('• [LOW] ', '')
                        top_changes.append(clean_rec[:60])
                
                changes_text = '; '.join(top_changes)
                edit_prompt = f"""Transform this room to {style_instruction}: {changes_text}. Maintain room layout and camera angle."""
            else:
                edit_prompt = f"""Transform this room to {style_instruction} with furniture changes, new decor, and styling updates."""
            
            # Truncate if too long
            if len(edit_prompt) > 1000:
                edit_prompt = edit_prompt[:950] + "..."
            
            print(f"🎨 Edit prompt: {edit_prompt}")
            
            # Use Image Edit API
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            with open(prepared_image_path, 'rb') as image_file:
                files = {
                    'image': image_file,
                    'prompt': (None, edit_prompt),
                    'n': (None, '1'),
                    'size': (None, '1024x1024'),
                    'model': (None, 'gpt-image-1'),
                    'input_fidelity': (None, 'high')  # Use high fidelity for better preservation
                }
                
                response = requests.post(
                    "https://api.openai.com/v1/images/edits",
                    headers=headers,
                    files=files,
                    timeout=120
                )
            
            # Clean up temporary file
            if prepared_image_path != image_path:
                os.remove(prepared_image_path)
            
            if not response.ok:
                error_details = response.text
                raise Exception(f"Image Edit API Error: {response.status_code} - {error_details}")
            
            result = response.json()
            print(f"🔍 API Response keys: {list(result.keys())}")
            
            # Extract image data
            if 'data' in result and len(result['data']) > 0:
                data_item = result['data'][0]
                
                # Check if we have URL or base64 data
                if 'url' in data_item:
                    print(f"✅ GPT Image 1 edit successful (URL)")
                    return data_item['url']
                elif 'b64_json' in data_item:
                    print(f"✅ GPT Image 1 edit successful (base64)")
                    # Convert base64 to temporary file and return path
                    import base64
                    import tempfile
                    
                    b64_data = data_item['b64_json']
                    image_data = base64.b64decode(b64_data)
                    
                    # Create temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                        temp_file.write(image_data)
                        temp_path = temp_file.name
                    
                    # We need to return a URL-like response, so let's save it properly
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    final_path = f"gpt_image_1_edit_{timestamp}.png"
                    
                    with open(final_path, 'wb') as f:
                        f.write(image_data)
                    
                    # Clean up temp file
                    os.remove(temp_path)
                    
                    # Return the local file path as if it were a URL (the download function will handle it)
                    return f"file://{os.path.abspath(final_path)}"
                else:
                    raise Exception(f"No URL or base64 data in response. Keys: {list(data_item.keys())}")
            else:
                raise Exception("No edited image returned from API")
                
        except Exception as e:
            raise Exception(f"Error generating standard pathway variation: {str(e)}")
    
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
    
    def generate_design(self, 
                       image_path: str, 
                       design_style: str = "modern",
                       custom_instructions: str = "",
                       design_type: str = "interior redesign",
                       edit_mode: str = "edit",
                       num_variations: int = 1) -> Dict[str, Any]:
        """Complete standard pathway design generation: analyze + generate AI-imagined products"""
        
        try:
            print("🔍 Step 1: Analyzing original image with GPT-4o Vision...")
            
            # Step 1: Analyze the original image
            analysis_results = self.analyze_image(
                image_path=image_path,
                design_style=design_style,
                custom_instructions=custom_instructions,
                design_type=design_type
            )
            
            print("✅ Analysis complete!")
            print(f"🎨 Design Style: {analysis_results.get('designConcept', {}).get('style', 'Unknown')}")
            print(f"📋 Recommendations: {len(analysis_results.get('recommendations', []))}")
            
            if edit_mode == "edit":
                print(f"🎨 Step 2: Generating AI-imagined products with GPT Image 1...")
                
                # Step 2: Generate AI-imagined products
                image_url = self.generate_variation(image_path, analysis_results)
                
                # Step 3: Download the generated image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"transformed_{timestamp}.png"
                
                print(f"💾 Step 3: Downloading generated image...")
                downloaded_path = self.download_image(image_url, output_filename)
                
                # Add generation info to results
                analysis_results['generatedImage'] = {
                    'url': image_url,
                    'localPath': downloaded_path,
                    'filename': output_filename,
                    'generatedAt': timestamp,
                    'method': 'standard_pathway_ai_imagined_products',
                    'pathway': 'standard'
                }
                
                print(f"✅ Standard pathway design saved as: {output_filename}")
            
            return analysis_results
            
        except Exception as e:
            raise Exception(f"Error in standard pathway design generation: {str(e)}") 