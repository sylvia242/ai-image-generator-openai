#!/usr/bin/env python3
"""
SerpAPI Google Shopping List Generator
Creates shopping lists from SerpAPI Google Shopping results with working product links
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

def create_serpapi_shopping_list(results_file: str = "design_results.json") -> str:
    """Create shopping list from SerpAPI Google Shopping products used in the design"""
    
    if not os.path.exists(results_file):
        print(f"❌ Error: Results file '{results_file}' not found")
        return None
    
    # Load the results
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    # Check if this was a SerpAPI pathway
    if 'serpapiProductsComposition' not in results:
        print("❌ Error: This doesn't appear to be a SerpAPI pathway result")
        return None
    
    serpapi_products = results['serpapiProductsComposition']['products_info']
    
    if not serpapi_products:
        print("❌ Error: No SerpAPI Google Shopping products found in results")
        return None
    
    print(f"🛒 Creating shopping list from {len(serpapi_products)} SerpAPI Google Shopping products...")
    
    # Create shopping_lists directory if it doesn't exist
    shopping_lists_dir = "shopping_lists"
    if not os.path.exists(shopping_lists_dir):
        os.makedirs(shopping_lists_dir)
    
    # Generate timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join(shopping_lists_dir, f"serpapi_shopping_list_{timestamp}.html")
    
    # Create HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SerpAPI Google Shopping Products - Your AI Design</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .products-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            padding: 40px;
        }}
        
        .product-card {{
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .product-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }}
        
        .product-image {{
            width: 100%;
            height: 250px;
            object-fit: cover;
            background: #f8f9fa;
        }}
        
        .product-info {{
            padding: 25px;
        }}
        
        .product-name {{
            font-size: 1.3em;
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
            line-height: 1.3;
        }}
        
        .product-area {{
            color: #667eea;
            font-weight: 600;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 15px;
        }}
        
        .product-price {{
            font-size: 1.5em;
            font-weight: 700;
            color: #28a745;
            margin-bottom: 10px;
        }}
        
        .product-rating {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .stars {{
            color: #ffd700;
            font-size: 1.2em;
            margin-right: 10px;
        }}
        
        .rating-text {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .product-retailer {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 15px;
        }}
        
        .product-description {{
            color: #666;
            line-height: 1.5;
            margin-bottom: 20px;
        }}
        
        .buy-button {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            padding: 12px 25px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s ease;
            text-align: center;
            width: 100%;
        }}
        
        .buy-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #666;
        }}
        
        .footer p {{
            margin-bottom: 10px;
        }}
        
        .serpapi-badge {{
            display: inline-block;
            background: #4285f4;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛒 SerpAPI Google Shopping Products</h1>
            <p>Real products found via SerpAPI and layered into your AI-generated design</p>
        </div>
        
        <div class="products-grid">
"""
    
    # Add each SerpAPI Google Shopping product
    for i, product in enumerate(serpapi_products, 1):
        area = product.get('area', 'General')
        name = product.get('name', 'Unknown Product')
        url = product.get('product_url', '#')
        price = product.get('price')
        retailer = product.get('retailer', 'Online Store')
        rating = product.get('rating')
        reviews = product.get('reviews')
        permanent_image_path = product.get('permanent_image_path', '')
        
        # Get product image
        product_image = ""
        if permanent_image_path and os.path.exists(permanent_image_path):
            # Convert local file path to data URL for HTML
            import base64
            try:
                print(f"   📸 Loading product image: {permanent_image_path}")
                with open(permanent_image_path, 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')
                    product_image = f"data:image/jpeg;base64,{img_data}"
                print(f"   ✅ Successfully loaded image for: {name}")
            except Exception as e:
                print(f"   ❌ Could not load product image {permanent_image_path}: {e}")
                product_image = "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=400&fit=crop"
        else:
            print(f"   ⚠️  No image found for: {name}")
            product_image = "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=400&fit=crop"
        
        # Format price
        price_display = f"${price:.2f}" if price else "Price not available"
        
        # Format rating
        rating_display = ""
        if rating:
            stars = "★" * int(rating) + "☆" * (5 - int(rating))
            reviews_text = f"({reviews} reviews)" if reviews else ""
            rating_display = f'<div class="product-rating"><span class="stars">{stars}</span><span class="rating-text">{rating}/5 {reviews_text}</span></div>'
        
        # Create product card HTML
        html_content += f"""
            <div class="product-card">
                <img src="{product_image}" alt="{name}" class="product-image">
                <div class="product-info">
                    <div class="product-area">{area}</div>
                    <h3 class="product-name">{name}</h3>
                    {rating_display}
                    <div class="product-price">{price_display}</div>
                    <div class="product-retailer">🏪 {retailer}</div>
                    <a href="{url}" target="_blank" class="buy-button">🛒 Buy Now</a>
                </div>
            </div>
        """
    
    # Close HTML
    html_content += """
        </div>
        
        <div class="footer">
            <p><strong>Generated from your AI design analysis</strong></p>
            <p>All products found via SerpAPI Google Shopping</p>
            <p><span class="serpapi-badge">Powered by SerpAPI</span></p>
        </div>
    </div>
</body>
</html>
"""
    
    # Save HTML file
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ SerpAPI shopping list saved as: {output_filename}")
    print("🎉 Success! Your SerpAPI Google Shopping products list is ready!")
    print(f"📂 File: {output_filename}")
    print("🛒 Each product links to the actual item found via SerpAPI!")
    print("🖼️ Product images show exactly what was layered!")
    print("⭐ Ratings and reviews included!")
    
    # Open in browser
    try:
        import webbrowser
        webbrowser.open(f"file://{os.path.abspath(output_filename)}")
        print("🌐 Opened in browser!")
    except:
        print("📂 Please open the HTML file manually in your browser")
    
    return output_filename

if __name__ == "__main__":
    create_serpapi_shopping_list() 