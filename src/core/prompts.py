#!/usr/bin/env python3
"""
Prompt templates for AI Image Generator
All prompts are centralized here for easy editing and maintenance
"""

def create_analysis_prompt(design_style: str = "modern", 
                          custom_instructions: str = "",
                          design_type: str = "interior redesign",
                          room_type: str = "") -> str:
    """Create the AI prompt for image analysis"""
    
    room_context = f"Room Type: {room_type.replace('-', ' ').title()}\n" if room_type else ""
    
    prompt = f"""As a professional design expert, analyze the provided image and create a detailed design transformation plan. Here are the requirements:

{room_context}Design Style: {design_style}
Design Type: {design_type}
Custom Instructions: {custom_instructions if custom_instructions else 'Create a comprehensive design transformation with multiple product categories including plants, artwork, storage, lighting, textiles, books, and decorative accessories for styling shelves, tables, and consoles'}

IMPORTANT: I have uploaded an image of the current space/object. Please carefully analyze this image to understand:
- Current layout, structure, and spatial arrangements
- Existing elements, furniture, colors, and materials
- Lighting conditions and architectural features
- Overall condition and any issues that need addressing
- Functional aspects and flow
- Style and aesthetic elements

DESIGN PHILOSOPHY: Focus on creating a comprehensive design transformation through strategic additions and styling enhancements. 
Emphasize a wide variety of decorative elements, accessories, lighting, textiles, plants, artwork, storage solutions, books, and styling elements that can transform the space into a well-curated, lived-in environment. Pay special attention to styling empty or sparse shelves, surfaces, and consoles with carefully selected decorative items.

COMPREHENSIVE PRODUCT CATEGORIES: Include a wide variety of product categories to create a complete design transformation:
- Plants (indoor plants, planters, plant stands, hanging plants)
- Artwork (wall art, prints, paintings, photography, sculptural pieces)
- Storage (decorative baskets, storage ottomans, floating shelves, bookcases, console organization)
- Lighting (table lamps, floor lamps, pendant lights, accent lighting, candles, string lights)
- Textiles (throw pillows, blankets, curtains, rugs, table runners, wall hangings)
- Books (decorative books, coffee table books, bookends)
- Decor for tables, shelves, and consoles (vases, decorative objects, trays, bowls, candlesticks, picture frames)
- Functional accessories (mirrors, clocks, decorative hardware)

STYLING GUIDELINES: 
- If shelves or surfaces appear unstyled or sparse, suggest specific styling elements to make them more visually appealing
- Even if items already exist in a category, you can suggest additional complementary items from the same category to enhance the overall design
- Focus on layering and creating visual interest through varied heights, textures, and groupings
- Consider seasonal or themed styling opportunities

Based on your analysis, please provide:
1. A detailed assessment of the current state
2. A comprehensive design transformation concept focusing on decor and styling
3. Specific recommendations prioritizing decorative elements, accessories, and enhancements
4. Color palette and material suggestions
5. Lighting and styling optimization ideas
6. Estimated transformation impact and benefits

RECOMMENDATION PRIORITIES:
- HIGH: Essential changes for immediate impact (lighting, plants, key artwork, textiles, storage solutions)
- MEDIUM: Important enhancements (decorative accessories, books, styling elements for shelves and surfaces, additional textiles)
- LOW: Nice-to-have finishing touches (candles, small decorative objects, seasonal elements)

COMPREHENSIVE STYLING APPROACH: Always include recommendations from multiple categories to create a complete, well-styled space. Aim for 8-12 different product types minimum to provide sufficient variety and styling options.

EXISTING ELEMENT ANALYSIS:
Before making recommendations, carefully identify and list all existing elements in the room:
- Existing furniture pieces and their condition
- Current window treatments (curtains, blinds, etc.)
- Existing lighting fixtures and their adequacy
- Current decorative elements and accessories
- Floor coverings and their condition
- Wall treatments and artwork
- Unstyled or sparse areas that need attention (empty shelves, bare surfaces, etc.)

ENHANCEMENT APPROACH: You can suggest items from the same category as existing elements to create layering, visual interest, and improved styling. For example:
- If there's already one piece of artwork, suggest additional pieces to create a gallery wall
- If there are some plants, suggest more plants or different types to create a lush environment
- If shelves exist but appear empty or sparse, suggest specific items to style them beautifully
- If there's basic lighting, suggest additional accent lighting for ambiance

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
- "Snake plant in 8-inch white ceramic planter, 24-30 inches tall, modern minimalist style"
- "Set of 3 framed botanical prints, 11x14 inches, black frames, green and white color scheme"
- "Woven storage baskets set of 2, natural rattan, 12-inch and 10-inch diameter, with handles"
- "Coffee table books set of 3, architecture and design themes, hardcover, neutral spines"
- "Brass candlestick holders set of 3, varying heights 6-10 inches, vintage inspired"

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
    "styling": "styling and decor recommendations",
    "roomAnalysis": {{
        "roomType": "specific room type (e.g., 'living room', 'bedroom', 'dining room')",
        "existingFurniture": ["list of existing furniture pieces"],
        "existingWindowTreatments": ["list of existing curtains, blinds, or window coverings"],
        "existingLighting": ["list of existing lighting fixtures"],
        "existingDecor": ["list of existing decorative elements and accessories"],
        "existingFloorCoverings": ["list of existing rugs, carpets, or floor treatments"],
        "existingWallTreatments": ["list of existing wall art, paint, or wall treatments"],
        "colorScheme": ["current color scheme"],
        "mood": "overall mood or atmosphere (e.g., 'cozy', 'bright', 'minimalist', 'warm')",
        "styleDetails": ["specific style elements like 'mid-century', 'industrial', 'coastal']",
        "architecturalFeatures": ["list of architectural features"],
        "lightingConditions": "current lighting situation"
    }}
}}"""
    
    return prompt





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
- Do not add any other items beyond the specified products
- Work with existing elements - if the room already has suitable curtains, lighting, or furniture, integrate new products to complement rather than replace them
- Focus on enhancing existing elements rather than replacing them"""
    
    return prompt 