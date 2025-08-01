#!/usr/bin/env python3
"""
AI Image Generator - Main Interface
Provides a unified interface for both standard and real products pathways
"""

import os
import json
import argparse
from typing import Dict, Any
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config_settings import get_api_key, get_serpapi_key
from src.core.real_products_pathway import RealProductsPathway


class AIImageGenerator:
    """Main AI Image Generator with support for both pathways"""
    
    def __init__(self, api_key: str):
        """Initialize the AI Image Generator with OpenAI API key"""
        self.api_key = api_key
        self.real_products_pathway = RealProductsPathway(api_key)
    
    def generate_design(self, 
                       image_path: str, 
                       design_style: str = "modern",
                       custom_instructions: str = "",
                       design_type: str = "interior redesign",
                       edit_mode: str = "edit",
                       num_variations: int = 1) -> Dict[str, Any]:
        """Generate design using real products pathway"""
        return self.real_products_pathway.generate_design_with_real_products(
            image_path=image_path,
            design_style=design_style,
            custom_instructions=custom_instructions,
            design_type=design_type,
            serpapi_key=get_serpapi_key()
        )
    
    def generate_design_with_real_products(self, 
                                         image_path: str, 
                                         design_style: str = "modern",
                                         custom_instructions: str = "",
                                         design_type: str = "interior redesign",
                                         fast_mode: bool = False) -> Dict[str, Any]:
        """Generate design using real products pathway (actual product images)"""
        return self.real_products_pathway.generate_design_with_real_products(
            image_path=image_path,
            design_style=design_style,
            custom_instructions=custom_instructions,
            design_type=design_type,
            fast_mode=fast_mode
        )
    
    def save_results(self, results: Dict[str, Any], output_file: str = "design_results.json"):
        """Save the design results to a JSON file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"✅ Results saved to {output_file}")
        except Exception as e:
            print(f"❌ Error saving results: {str(e)}")
    
    def print_results(self, results: Dict[str, Any]):
        """Print a summary of the design results"""
        if not results:
            print("❌ No results to display")
            return
        
        print("\n" + "="*60)
        print("🎨 DESIGN ANALYSIS RESULTS")
        print("="*60)
        
        # Design Concept
        design_concept = results.get('designConcept', {})
        if design_concept:
            print(f"🎨 Style: {design_concept.get('style', 'Unknown')}")
            print(f"🎨 Color Palette: {', '.join(design_concept.get('colorPalette', []))}")
            print(f"🎨 Materials: {', '.join(design_concept.get('materials', []))}")
        
        # Recommendations
        recommendations = results.get('recommendations', [])
        if recommendations:
            print(f"\n📋 Recommendations ({len(recommendations)}):")
            for i, rec in enumerate(recommendations[:5], 1):  # Show first 5
                priority = rec.get('priority', 'Unknown')
                area = rec.get('area', 'General')
                description = rec.get('description', 'No description')[:100]
                print(f"   {i}. [{priority}] {area}: {description}...")
        
        # Generated Image Info
        if 'generatedImage' in results:
            img_info = results['generatedImage']
            print(f"\n🖼️  Generated Image:")
            print(f"   📁 File: {img_info.get('filename', 'Unknown')}")
            print(f"   🔗 URL: {img_info.get('url', 'Local file')}")
            print(f"   🛤️  Pathway: {img_info.get('pathway', 'Unknown')}")
        
        # Real Products Info
        if 'serpapiProductsComposition' in results:
            comp_info = results['serpapiProductsComposition']
            print(f"\n🛒 Real Products Used:")
            print(f"   📦 Products: {comp_info.get('products_used', 0)}")
            print(f"   🛤️  Method: {comp_info.get('method', 'Unknown')}")
            
            products_info = comp_info.get('products_info', [])
            if products_info:
                print(f"   📋 Product Details:")
                for i, product in enumerate(products_info[:3], 1):  # Show first 3
                    name = product.get('name', 'Unknown')
                    price = product.get('price', 'Unknown')
                    retailer = product.get('retailer', 'Unknown')
                    print(f"      {i}. {name} - ${price} ({retailer})")
        
        print("\n" + "="*60)


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
    parser.add_argument("--pathway", choices=["standard", "real_products"], default="real_products", help="Design pathway: real_products (use actual product images)")
    parser.add_argument("--variations", type=int, default=1, help="Number of variations to create (1-4, only used with --mode variations)")
    parser.add_argument("--fast", action="store_true", help="Enable fast mode for quicker processing (reduced quality)")
    
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
        if args.fast:
            print(f"⚡ Fast mode: ENABLED (quicker processing, reduced quality)")
        else:
            print(f"⚡ Fast mode: DISABLED (full quality processing)")
        if args.instructions:
            print(f"💭 Custom instructions: {args.instructions}")
        
        if args.analysis_only:
            print("📋 Mode: Analysis only (no image transformation)")
            edit_mode = None
        else:
            print(f"🔧 Mode: {args.mode}")
            print(f"🛤️  Pathway: {args.pathway}")
            edit_mode = args.mode
        
        # Generate design using the appropriate pathway
        if args.pathway == "real_products" and not args.analysis_only:
            print("🛒 Using real products pathway...")
            results = generator.generate_design_with_real_products(
                image_path=args.image_path,
                design_style=args.style,
                custom_instructions=args.instructions,
                design_type=args.type,
                fast_mode=args.fast
            )
        else:
            print("🎨 Using standard pathway...")
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