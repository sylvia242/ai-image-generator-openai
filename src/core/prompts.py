#!/usr/bin/env python3
"""
Prompt templates for AI Image Generator
All prompts are centralized here for easy editing and maintenance
"""

def create_analysis_prompt(design_style: str = "modern", 
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

Focus heavily on suggesting VERY SPECIFIC decorative products with exact details for accurate shopping:

For each recommendation, include:
- EXACT product specifications (sizes, dimensions, materials, colors, patterns)
- SPECIFIC style descriptors (modern boho, vintage industrial, scandinavian minimalist)
- BRAND/STYLE examples when relevant
- QUANTITY needed
- PLACEMENT details

Examples of SPECIFIC recommendations:
- "2-3 square throw pillows, 18x18 inches, terracotta linen texture and teal velvet with tassel trim"
- "Rattan floor lamp, 60-65 inches tall, natural woven shade, black metal base, bohemian style"
- "Macrame wall hanging, 24x36 inches, natural cotton cord, geometric diamond pattern"
- "Ceramic vases set of 3, earth tones (terracotta, sage, cream), 6-12 inch heights, matte finish"
- "Jute area rug, 5x8 feet, natural fiber with geometric border pattern in rust/teal"

Only suggest furniture replacement as a last resort - instead focus on how to style, accessorize, or modify existing pieces with SPECIFIC PRODUCTS.

Format the response as JSON with this exact structure:
{{
    "designConcept": {{
        "style": "string",
        "colorPalette": ["array", "of", "colors"],
        "materials": ["array", "of", "materials"],
        "overallAssessment": "detailed assessment of current state",
        "transformationConcept": "comprehensive design transformation concept"
    }},
    "recommendations": [
        {{
            "area": "specific area (e.g., 'Seating Area', 'Lighting', 'Wall Decor')",
            "type": "product type (e.g., 'throw pillows', 'floor lamp', 'wall art')",
            "description": "detailed product description with exact specifications",
            "priority": "High/Medium/Low",
            "estimatedCost": "cost range",
            "placement": "specific placement instructions"
        }}
    ],
    "colorPalette": {{
        "primary": ["main colors"],
        "accent": ["accent colors"],
        "neutral": ["neutral colors"]
    }},
    "materials": ["list", "of", "materials"],
    "lighting": "lighting recommendations",
    "styling": "styling and decor recommendations"
}}"""
    
    return prompt


def create_standard_pathway_prompt(analysis_results: dict, design_style: str) -> str:
    """Create prompt for standard pathway (AI-imagined products)"""
    
    # Extract key information from analysis
    recommendations = analysis_results.get('recommendations', [])
    color_palette = analysis_results.get('colorPalette', {}).get('primary', [])
    materials = analysis_results.get('materials', [])
    
    # Create style-specific instructions
    style_instruction = f"Transform this room to {design_style} style"
    
    # Build comprehensive generation prompt
    generation_prompt = f"""Transform this interior design to {design_style} style with comprehensive improvements.

STYLE REQUIREMENTS:
- {style_instruction}
- Use {', '.join(color_palette) if color_palette else 'appropriate'} color palette
- Incorporate {', '.join(materials) if materials else 'quality'} materials
- Maintain professional interior design quality
- Keep the same room layout and camera perspective

TRANSFORMATION REQUIREMENTS:
- Implement ALL recommendations with visible changes
- Allow furniture repositioning, replacement, and restyling as needed
- Create a cohesive {design_style} aesthetic
- Maintain the same room layout and camera perspective
- Create a cohesive {design_style.lower()} aesthetic with professional interior design quality"""
    
    return generation_prompt


def create_real_products_pathway_prompt(products: list) -> str:
    """Create prompt for real products pathway (multi-image approach)"""
    
    # Create product descriptions
    product_descriptions = []
    for i, product in enumerate(products, 1):
        area = product.get('area', 'General')
        name = product.get('name', 'Unknown Product')
        price = product.get('price')
        retailer = product.get('retailer', 'Online Store')
        
        price_info = f" (${price})" if price else ""
        product_descriptions.append(f"{i}. {name} - {area} - {retailer}{price_info}")
    
    # Create comprehensive prompt
    prompt = f"""Transform this interior design by adding these real products naturally into the room:

REAL PRODUCTS TO ADD:
{chr(10).join(product_descriptions)}

CRITICAL INSTRUCTIONS:
- The first image shows the room to transform
- The additional images show the real products to integrate
- Add each product naturally to the appropriate area of the room
- Maintain the original room structure, lighting, and perspective
- Use the exact products shown in the additional images - do not modify their appearance
- Place products in realistic, functional positions
- Keep the overall design cohesive and professional
- Do not add any other items beyond the specified products"""
    
    return prompt 