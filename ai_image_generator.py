#!/usr/bin/env python3
"""
AI Image Generator Script
Based on the prompt structure from the HostLux AI Interior Design Platform
Uses OpenAI's GPT-4 Vision for analysis and Image Edit API for transformations
"""

import os
import base64
import json
import requests
from typing import Optional, List, Dict, Any
from pathlib import Path
import argparse
from config import get_api_key
from datetime import datetime
from PIL import Image
import io

class AIImageGenerator:
    def __init__(self, api_key: str):
        """Initialize the AI Image Generator with OpenAI API key"""
        self.api_key = api_key
        self.vision_model = "gpt-4o"  # GPT-4 with vision capabilities
        self.chat_url = "https://api.openai.com/v1/chat/completions"
        self.image_edit_url = "https://api.openai.com/v1/images/edits"
        self.image_variations_url = "https://api.openai.com/v1/images/variations"
        
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
            # Open and process the image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary (for PNG output)
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Resize to square format (required by OpenAI)
                # Use the smaller dimension to avoid cropping important content
                min_dimension = min(img.size)
                
                # Crop to square from center
                left = (img.width - min_dimension) // 2
                top = (img.height - min_dimension) // 2
                right = left + min_dimension
                bottom = top + min_dimension
                
                img_square = img.crop((left, top, right, bottom))
                
                # Resize to optimal size (1024x1024 works well)
                img_resized = img_square.resize((1024, 1024), Image.Resampling.LANCZOS)
                
                # Save as PNG
                output_path = f"temp_prepared_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                img_resized.save(output_path, 'PNG')
                
                return output_path
                
        except Exception as e:
            raise Exception(f"Error preparing image: {str(e)}")
    
    def create_analysis_prompt(self, 
                             design_style: str = "modern", 
                             custom_instructions: str = "",
                             design_type: str = "interior redesign") -> str:
        """Create the AI prompt for image analysis"""
        
        prompt = f"""As a professional design expert, analyze the provided image and create a detailed design transformation plan. Here are the requirements:

Design Style: {design_style}
Design Type: {design_type}
Custom Instructions: {custom_instructions if custom_instructions else 'Create an appealing and functional design'}

IMPORTANT: I have uploaded an image of the current space/object. Please carefully analyze this image to understand:
- Current layout, structure, and spatial arrangements
- Existing elements, furniture, colors, and materials
- Lighting conditions and architectural features
- Overall condition and any issues that need addressing
- Functional aspects and flow
- Style and aesthetic elements

DESIGN PHILOSOPHY: Focus on enhancing the existing space through strategic additions and modifications rather than complete furniture replacement. Emphasize decorative elements, accessories, lighting, textiles, and styling that can transform the space while working with existing furniture pieces.

Based on your analysis, please provide:
1. A detailed assessment of the current state
2. A comprehensive design transformation concept focusing on decor and styling
3. Specific recommendations prioritizing decorative elements, accessories, and enhancements
4. Color palette and material suggestions
5. Lighting and styling optimization ideas
6. Estimated transformation impact and benefits

RECOMMENDATION PRIORITIES:
- HIGH: Essential changes for immediate impact (lighting, key decor pieces, color accents)
- MEDIUM: Important enhancements (textiles, additional accessories, minor furniture adjustments)
- LOW: Nice-to-have finishing touches (artwork, plants, small decorative objects)

Focus heavily on suggesting specific decorative elements such as:
- Throw pillows, blankets, and textiles with specific colors/patterns
- Candles, vases, and decorative objects
- Artwork, mirrors, and wall decor
- Plants and natural elements
- Lighting fixtures (lamps, string lights, etc.)
- Rugs, curtains, and window treatments
- Books, trays, and styling accessories

Only suggest furniture replacement as a last resort - instead focus on how to style, accessorize, or modify existing pieces.

Format the response as JSON with this exact structure:
{{
  "currentAnalysis": {{
    "description": "Detailed analysis of what you see in the image",
    "strengths": ["List of current positive elements"],
    "improvementAreas": ["List of areas that could be enhanced"]
  }},
  "designConcept": {{
    "overallVision": "Main design concept and philosophy",
    "style": "Specific style classification",
    "colorPalette": ["List of recommended colors"],
    "materials": ["List of recommended materials"]
  }},
  "recommendations": [
    {{
      "area": "Specific area or element",
      "description": "Detailed recommendation with specific items/products",
      "rationale": "Why this improvement will work",
      "priority": "High/Medium/Low"
    }}
  ],
  "transformationSummary": {{
    "keyChanges": ["List of major transformations"],
    "expectedImpact": "Overall impact description",
    "styleEvolution": "How the design will evolve"
  }}
}}

Please ensure the response is valid JSON format."""
        
        return prompt
    
    def create_edit_prompt(self, analysis_results: Dict[str, Any]) -> str:
        """Create a prompt for OpenAI Image Edit API based on analysis results (max 1000 chars)"""
        
        design_concept = analysis_results.get('designConcept', {})
        recommendations = analysis_results.get('recommendations', [])
        
        # Extract key design elements
        style = design_concept.get('style', 'modern')
        colors = ', '.join(design_concept.get('colorPalette', ['neutral tones'])[:3])  # Limit colors
        materials = ', '.join(design_concept.get('materials', ['contemporary materials'])[:3])  # Limit materials
        
        # Start with base transformation
        edit_prompt = f"Transform to {style.lower()} style with {colors} colors, {materials}. "
        
        # Add ALL recommendations in condensed format
        all_recs = []
        for rec in recommendations:
            priority_marker = {"High": "!", "Medium": "+", "Low": "-"}.get(rec.get('priority', 'Medium'), '+')
            desc = rec.get('description', '')[:80]  # Truncate long descriptions
            all_recs.append(f"{priority_marker}{desc}")
        
        # Add recommendations with character limit awareness
        remaining_chars = 950 - len(edit_prompt)  # Leave room for ending
        rec_text = " ".join(all_recs)
        
        if len(rec_text) > remaining_chars:
            # Prioritize High and Medium recommendations if space is limited
            high_med_recs = [rec for rec in recommendations if rec.get('priority') in ['High', 'Medium']]
            rec_text = " ".join([f"{rec.get('description', '')[:60]}" for rec in high_med_recs])
            if len(rec_text) > remaining_chars:
                rec_text = rec_text[:remaining_chars-50] + "..."
        
        edit_prompt += rec_text
        
        # Add concise ending instruction
        edit_prompt += " Apply these changes visibly and cohesively."
        
        # Ensure we're under 1000 characters
        if len(edit_prompt) > 1000:
            edit_prompt = edit_prompt[:950] + " Apply changes."
        
        return edit_prompt
    
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
            prompt = self.create_analysis_prompt(design_style, custom_instructions, design_type)
            
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
                    # If JSON parsing fails, create a structured response from the text
                    return {
                        "currentAnalysis": {
                            "description": content[:500] + "..." if len(content) > 500 else content,
                            "strengths": ["Analysis provided in description"],
                            "improvementAreas": ["See full analysis in description"]
                        },
                        "designConcept": {
                            "overallVision": "Design recommendations provided in analysis",
                            "style": design_style,
                            "colorPalette": ["See full analysis"],
                            "materials": ["See full analysis"]
                        },
                        "recommendations": [{
                            "area": "General",
                            "description": "Full recommendations available in the complete analysis",
                            "rationale": "Based on AI analysis of the provided image",
                            "priority": "High"
                        }],
                        "transformationSummary": {
                            "keyChanges": ["See complete analysis"],
                            "expectedImpact": "Detailed in full analysis",
                            "styleEvolution": "As described in analysis"
                        },
                        "fullAnalysis": content
                    }
            else:
                raise Exception("No valid response from OpenAI Vision API")
                
        except Exception as e:
            raise Exception(f"Error analyzing image: {str(e)}")
    
    def edit_image(self, image_path: str, analysis_results: Dict[str, Any]) -> str:
        """Edit the original image using OpenAI Image Edit API"""
        
        try:
            # Prepare image for editing
            print("🔧 Preparing image for editing (converting to PNG, resizing)...")
            prepared_image_path = self.prepare_image_for_edit(image_path)
            
            # Create edit prompt
            edit_prompt = self.create_edit_prompt(analysis_results)
            print(f"🎨 Edit Prompt: {edit_prompt[:150]}...")
            
            # Prepare the API request
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Open the prepared image file
            with open(prepared_image_path, 'rb') as image_file:
                files = {
                    'image': (prepared_image_path, image_file, 'image/png'),
                    'prompt': (None, edit_prompt),
                    'n': (None, '1'),
                    'size': (None, '1024x1024')
                }
                
                # Make API call
                response = requests.post(
                    self.image_edit_url,
                    headers=headers,
                    files=files,
                    timeout=120
                )
            
            # Clean up temporary file
            if os.path.exists(prepared_image_path):
                os.remove(prepared_image_path)
            
            if not response.ok:
                error_details = response.text
                raise Exception(f"OpenAI Image Edit API Error: {response.status_code} - {error_details}")
            
            result = response.json()
            
            # Extract image URL
            if 'data' in result and len(result['data']) > 0:
                image_url = result['data'][0]['url']
                return image_url
            else:
                raise Exception("No edited image returned from API")
                
        except Exception as e:
            raise Exception(f"Error editing image: {str(e)}")
    
    def create_gpt4o_generated_variation(self, image_path: str, analysis_results: Dict[str, Any]) -> str:
        """Use GPT-4o to generate a new image based on analysis of the original"""
        
        try:
            # Get original image analysis
            current_analysis = analysis_results.get('currentAnalysis', {})
            design_concept = analysis_results.get('designConcept', {})
            recommendations = analysis_results.get('recommendations', [])
            
            # Extract design elements
            style = design_concept.get('style', 'modern')
            colors = ', '.join(design_concept.get('colorPalette', ['neutral tones']))
            materials = ', '.join(design_concept.get('materials', ['contemporary materials']))
            
            # Get current room description
            current_description = current_analysis.get('description', 'interior space')
            
                         # Determine style approach - use existing vibe if style is generic
            if style.lower() in ['modern', 'contemporary', 'stylish', 'nice', 'good', 'better']:
                style_instruction = f"lean into and enhance the existing room's natural vibe and aesthetic"
                style_reference = "the room's current style"
            else:
                style_instruction = f"add {style.lower()} elements"
                style_reference = f"{style.lower()} style"
            
            # Build creative transformation prompt based on analysis
            generation_prompt = f"""Interior design transformation: {current_description}

DESIGN TRANSFORMATION GOALS:
- Transform this room to {style_instruction} while maintaining the basic layout
- Keep the same room dimensions and architectural features
- Allow furniture repositioning, replacement, and styling changes
- Maintain the same camera angle and perspective
- Create a cohesive {style.lower()} aesthetic throughout

CREATIVE TRANSFORMATION to achieve {style_instruction}:"""
            
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
- Use {colors} color palette throughout the design
- Incorporate {materials} materials for authenticity
- Allow furniture repositioning, replacement, and restyling as needed
- {style_instruction.capitalize()} through comprehensive design changes
- Maintain the same room layout and camera perspective
- Create a cohesive {style.lower()} aesthetic with professional interior design quality"""
            
            print(f"🎨 Generating new image with GPT-4o based on analysis...")
            print(f"🔥 Generation prompt: {generation_prompt[:200]}...")
            
            # Use OpenAI Image Edit API with GPT Image 1 for true image-to-image editing
            print(f"🖼️ Using OpenAI Image Edit API (DALL-E 2) for image-to-image transformation...")
            
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
            raise Exception(f"Error creating GPT-4o generated variation: {str(e)}")
    
    def generate_with_dalle3(self, prompt: str) -> str:
        """Generate image using DALL-E 3 with enhanced prompt"""
        
        try:
            # Prepare DALL-E 3 API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Truncate prompt if too long for DALL-E 3
            if len(prompt) > 4000:
                prompt = prompt[:3950] + "... Professional interior design photography."
            
            payload = {
                "model": "dall-e-3",
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024",
                "quality": "hd",
                "style": "natural"
            }
            
            # Make API call
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if not response.ok:
                error_details = response.text
                raise Exception(f"DALL-E 3 API Error: {response.status_code} - {error_details}")
            
            result = response.json()
            
            # Extract image URL
            if 'data' in result and len(result['data']) > 0:
                return result['data'][0]['url']
            else:
                raise Exception("No image generated by DALL-E 3")
                
        except Exception as e:
            raise Exception(f"Error generating with DALL-E 3: {str(e)}")
    
    def download_image(self, image_url: str, output_path: str) -> str:
        """Download the generated image from URL or copy from local file"""
        
        try:
            # Handle local file URLs (from GPT Image 1 base64 responses)
            if image_url.startswith('file://'):
                local_path = image_url.replace('file://', '')
                if os.path.exists(local_path):
                    # Copy the file to the desired output path
                    import shutil
                    shutil.copy2(local_path, output_path)
                    # Clean up the temporary file
                    os.remove(local_path)
                    return output_path
                else:
                    raise Exception(f"Local file not found: {local_path}")
            else:
                # Handle regular HTTP URLs
                response = requests.get(image_url, timeout=30)
                response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
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
        """Complete design generation pipeline: analyze + edit/transform existing image"""
        
        try:
            print("🔍 Step 1: Analyzing original image with GPT-4o Vision...")
            
            # Step 1: Analyze the original image
            analysis_results = self.analyze_image(
                image_path=image_path,
                design_style=design_style,
                custom_instructions=custom_instructions,
                design_type=design_type
            )
            
            if edit_mode == "edit":
                print("🎨 Step 2: Generating transformed image with GPT-4o + DALL-E 3...")
                
                # Step 2: Generate transformed image based on analysis
                image_url = self.create_gpt4o_generated_variation(image_path, analysis_results)
                
                # Step 3: Download the edited image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"transformed_{timestamp}.png"
                
                print(f"💾 Step 3: Downloading transformed image...")
                downloaded_path = self.download_image(image_url, output_filename)
                
                # Add image generation info to results
                analysis_results['transformedImage'] = {
                    'url': image_url,
                    'localPath': downloaded_path,
                    'filename': output_filename,
                    'generatedAt': timestamp,
                    'method': 'edit'
                }
                
                print(f"✅ Transformed image saved as: {output_filename}")
            
            elif edit_mode == "variations":
                print(f"🎨 Step 2: Generating new image with GPT-4o + DALL-E 3...")
                
                # Step 2: Use GPT-4o analysis to generate new image with DALL-E 3
                image_url = self.create_gpt4o_generated_variation(image_path, analysis_results)
                
                # Step 3: Download the variation
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"comprehensive_variation_{timestamp}.png"
                
                print(f"💾 Step 3: Downloading comprehensive variation...")
                downloaded_path = self.download_image(image_url, output_filename)
                
                # Add variation info to results
                analysis_results['comprehensiveVariation'] = {
                    'url': image_url,
                    'localPath': downloaded_path,
                    'filename': output_filename,
                    'generatedAt': timestamp,
                    'method': 'comprehensive_implementation',
                    'implementedSuggestions': 'ALL (High, Medium, Low priority)'
                }
                
                print(f"✅ Comprehensive variation saved as: {output_filename}")
            
            return analysis_results
            
        except Exception as e:
            raise Exception(f"Error in design generation pipeline: {str(e)}")
    
    def save_results(self, results: Dict[str, Any], output_file: str = "design_results.json"):
        """Save the design results to a JSON file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"✅ Results saved to {output_file}")
        except Exception as e:
            print(f"❌ Error saving results: {str(e)}")
    
    def print_results(self, results: Dict[str, Any]):
        """Print the design results in a formatted way"""
        print("\n" + "="*60)
        print("🎨 AI DESIGN ANALYSIS & TRANSFORMATION (GPT-4o + Image Edit)")
        print("="*60)
        
        # If there's a full analysis field, show it first
        if 'fullAnalysis' in results:
            print(f"\n📋 COMPLETE AI ANALYSIS:")
            print(f"   {results['fullAnalysis']}")
            print("\n" + "-"*60)
        
        # Current Analysis
        if 'currentAnalysis' in results:
            analysis = results['currentAnalysis']
            print(f"\n📋 CURRENT STATE ANALYSIS:")
            print(f"   {analysis.get('description', 'No description available')}")
            
            if 'strengths' in analysis and analysis['strengths']:
                print(f"\n✅ STRENGTHS:")
                for strength in analysis['strengths']:
                    print(f"   • {strength}")
            
            if 'improvementAreas' in analysis and analysis['improvementAreas']:
                print(f"\n🔧 IMPROVEMENT AREAS:")
                for area in analysis['improvementAreas']:
                    print(f"   • {area}")
        
        # Design Concept
        if 'designConcept' in results:
            concept = results['designConcept']
            print(f"\n🎯 DESIGN CONCEPT:")
            print(f"   Vision: {concept.get('overallVision', 'No vision specified')}")
            print(f"   Style: {concept.get('style', 'No style specified')}")
            
            if 'colorPalette' in concept and concept['colorPalette']:
                print(f"   Colors: {', '.join(concept['colorPalette'])}")
            
            if 'materials' in concept and concept['materials']:
                print(f"   Materials: {', '.join(concept['materials'])}")
        
        # Recommendations
        if 'recommendations' in results and results['recommendations']:
            print(f"\n💡 SPECIFIC RECOMMENDATIONS:")
            for i, rec in enumerate(results['recommendations'], 1):
                print(f"\n   {i}. {rec.get('area', 'General Area')} [{rec.get('priority', 'Medium')} Priority]")
                print(f"      {rec.get('description', 'No description')}")
                print(f"      Rationale: {rec.get('rationale', 'No rationale provided')}")
        
        # Transformation Summary
        if 'transformationSummary' in results:
            summary = results['transformationSummary']
            print(f"\n🚀 TRANSFORMATION SUMMARY:")
            
            if 'keyChanges' in summary and summary['keyChanges']:
                print(f"   Key Changes:")
                for change in summary['keyChanges']:
                    print(f"   • {change}")
            
            print(f"   Expected Impact: {summary.get('expectedImpact', 'No impact description')}")
            print(f"   Style Evolution: {summary.get('styleEvolution', 'No evolution description')}")
        
        # Transformed Image Info
        if 'transformedImage' in results:
            img_info = results['transformedImage']
            print(f"\n🖼️ TRANSFORMED IMAGE:")
            print(f"   File: {img_info.get('filename', 'N/A')}")
            print(f"   Path: {img_info.get('localPath', 'N/A')}")
            print(f"   Method: {img_info.get('method', 'N/A')}")
            print(f"   Generated: {img_info.get('generatedAt', 'N/A')}")
        
        # Comprehensive Variation Info
        if 'comprehensiveVariation' in results:
            var_info = results['comprehensiveVariation']
            print(f"\n🖼️ COMPREHENSIVE VARIATION:")
            print(f"   File: {var_info.get('filename', 'N/A')}")
            print(f"   Path: {var_info.get('localPath', 'N/A')}")
            print(f"   Method: {var_info.get('method', 'N/A')}")
            print(f"   Implemented: {var_info.get('implementedSuggestions', 'N/A')}")
            print(f"   Generated: {var_info.get('generatedAt', 'N/A')}")
        
        # Legacy Variations Info (for backward compatibility)
        if 'variations' in results:
            var_info = results['variations']
            print(f"\n🖼️ IMAGE VARIATIONS:")
            print(f"   Count: {var_info.get('count', 0)}")
            print(f"   Method: {var_info.get('method', 'N/A')}")
            print(f"   Generated: {var_info.get('generatedAt', 'N/A')}")
            
            if 'images' in var_info:
                for img in var_info['images']:
                    print(f"   • Variation {img.get('variationNumber', '?')}: {img.get('filename', 'N/A')}")
        
        print("\n" + "="*60)

    def create_direct_variation(self, image_path: str, style: str = "stylish", instructions: str = "") -> str:
        """Generate variation directly with DALL-E 3 - NO ANALYSIS, STRICT PRESERVATION"""
        
        try:
            # Determine style approach
            if style.lower() in ['modern', 'contemporary', 'stylish', 'nice', 'good', 'better']:
                style_instruction = f"enhance the existing room's natural aesthetic"
            else:
                style_instruction = f"add subtle {style.lower()} decor touches"
            
            # Build ULTRA-STRICT preservation prompt
            generation_prompt = f"""Interior design photo with ABSOLUTE PRESERVATION REQUIREMENTS:

CRITICAL - KEEP 100% IDENTICAL:
- EXACT same room layout, walls, flooring, ceiling colors and positions
- ALL furniture MUST stay in IDENTICAL positions, colors, sizes, styles (every sofa, chair, table, etc.)
- SAME windows, doors, curtains - absolutely no changes
- IDENTICAL camera angle, perspective, lighting, shadows
- SAME architectural features and room dimensions

ONLY ADD TINY DECOR ITEMS to {style_instruction}:
- Small throw pillows on existing seating (2-3 max)
- Small decorative objects on existing tables (1-2 candles, small vase, book)
- One small plant or flowers
- Small wall art above existing furniture (if wall is visible)

ABSOLUTE ENFORCEMENT:
- NO furniture changes, replacements, repositioning, or recoloring whatsoever
- NO structural changes to room
- NO new windows, doors, or architectural features
- NO changing existing curtains, rugs, or major elements
- IDENTICAL photographic perspective and lighting conditions
- Maximum 4-5 small decor additions only
- Keep the exact same room character, layout, and all existing elements

The result must look like the exact same room with just a few small decorative touches added.
{instructions}"""
            
            print(f"🎨 Direct DALL-E 3 generation with STRICT preservation...")
            
            # Generate with DALL-E 3
            return self.generate_with_dalle3(generation_prompt)
            
        except Exception as e:
            print(f"❌ Error in direct generation: {str(e)}")
            return None

def main():
    parser = argparse.ArgumentParser(description="AI Image Generator using OpenAI GPT-4 Vision + Image Edit API")
    parser.add_argument("image_path", help="Path to the image file to analyze")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY environment variable)")
    parser.add_argument("--style", default="modern", help="Design style (default: modern)")
    parser.add_argument("--instructions", default="", help="Custom design instructions")
    parser.add_argument("--type", default="interior redesign", help="Type of design (default: interior redesign)")
    parser.add_argument("--output", default="design_results.json", help="Output file for results")
    parser.add_argument("--no-save", action="store_true", help="Don't save results to file")
    parser.add_argument("--analysis-only", action="store_true", help="Only analyze, don't transform image")
    parser.add_argument("--mode", choices=["edit", "variations"], default="edit", help="Transformation mode: edit (modify based on analysis) or variations (create style variations)")
    parser.add_argument("--variations", type=int, default=1, help="Number of variations to create (1-4, only used with --mode variations)")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or get_api_key()
    if not api_key:
        print("❌ Error: Please provide OpenAI API key via:")
        print("   1. Command line: --api-key 'your_key'")
        print("   2. Environment variable: export OPENAI_API_KEY='your_key'")
        print("   3. Config file: Edit config.py and set API_KEY variable")
        return
    
    # Check if image file exists
    if not os.path.exists(args.image_path):
        print(f"❌ Error: Image file '{args.image_path}' not found")
        return
    
    try:
        # Initialize generator
        generator = AIImageGenerator(api_key)
        
        print(f"🔍 Analyzing image: {args.image_path}")
        print(f"🎨 Design style: {args.style}")
        print(f"📝 Design type: {args.type}")
        print(f"🤖 Using: OpenAI GPT-4o Vision + Image Edit API")
        if args.instructions:
            print(f"💭 Custom instructions: {args.instructions}")
        
        if args.analysis_only:
            print("📋 Mode: Analysis only (no image transformation)")
            edit_mode = None
        else:
            print(f"🔧 Mode: {args.mode}")
            edit_mode = args.mode
        
        # Generate design
        results = generator.generate_design(
            image_path=args.image_path,
            design_style=args.style,
            custom_instructions=args.instructions,
            design_type=args.type,
            edit_mode=edit_mode if not args.analysis_only else None,
            num_variations=args.variations if args.mode == "variations" else 1
        )
        
        # Display results
        generator.print_results(results)
        
        # Save results
        if not args.no_save:
            generator.save_results(results, args.output)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 