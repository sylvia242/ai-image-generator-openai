#!/usr/bin/env python3
"""
Main Entry Point for AI Image Generator
Demonstrates the reorganized project structure with separate pathway classes
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.ai_image_generator import AIImageGenerator
from config.config_settings import get_api_key, get_serpapi_key

def main():
    """Main entry point demonstrating the reorganized structure"""
    
    print("🎨 AI IMAGE GENERATOR - RESTRUCTURED ARCHITECTURE")
    print("="*60)
    
    # Check API keys
    openai_key = get_api_key()
    serpapi_key = get_serpapi_key()
    
    print(f"✅ OpenAI API Key: {'Configured' if openai_key else 'Missing'}")
    print(f"✅ SerpAPI Key: {'Configured' if serpapi_key else 'Missing'}")
    
    print("\n📁 NEW PROJECT STRUCTURE:")
    print("   src/")
    print("   ├── core/")
    print("   │   ├── ai_image_generator.py (Main interface)")
    print("   │   ├── standard_pathway.py (AI-imagined products)")
    print("   │   ├── real_products_pathway.py (Real product images)")
    print("   │   └── prompts.py (All prompt templates)")
    print("   ├── shopping/")
    print("   │   ├── shopping_list_generator.py")
    print("   │   ├── standard_pathway_shopping_list.py")
    print("   │   ├── serpapi_shopping_integration.py")
    print("   │   └── real_products_pathway_shopping_list.py")
    print("   └── utils/")
    print("       └── (utility functions)")
    print("   tests/")
    print("   ├── test_both_pathways_standard_and_real_products.py")
    print("   ├── test_real_products_analysis_only.py")
    print("   └── fixed_shopping_test_serpapi.py")
    print("   examples/")
    print("   ├── example_standard.py")
    print("   └── example_real_products.py")
    print("   config/")
    print("   ├── config_settings.py")
    print("   └── config_template.py")
    print("   shopping_lists/")
    print("   └── (generated HTML files)")
    
    print("\n🚀 AVAILABLE SCRIPTS:")
    print("   • python tests/test_both_pathways_standard_and_real_products.py - Test both pathways")
    print("   • python tests/test_real_products_analysis_only.py - Test analysis & shopping (no image)")
    print("   • python examples/example_standard.py - Standard pathway demo (AI-imagined products)")
    print("   • python examples/example_real_products.py - Real products pathway demo")
    print("   • python src/shopping/serpapi_shopping_integration.py - SerpAPI integration")
    
    print("\n🎯 NEW ARCHITECTURE BENEFITS:")
    print("   ✅ Clear separation between standard and real products pathways")
    print("   ✅ Centralized prompt management in prompts.py")
    print("   ✅ Each pathway has its own dedicated class")
    print("   ✅ Easy to edit prompts without touching core logic")
    print("   ✅ Maintainable and extensible codebase")
    print("   ✅ Unified interface through main AIImageGenerator class")
    
    print("\n🔧 PROMPT EDITING:")
    print("   📝 Edit src/core/prompts.py to modify all AI prompts")
    print("   📝 create_analysis_prompt() - For image analysis")
    print("   📝 create_standard_pathway_prompt() - For AI-imagined products")
    print("   📝 create_real_products_pathway_prompt() - For real products")
    
    print("\n✅ Project successfully restructured!")
    print("   All pathways now have clear separation and maintainable prompts")

if __name__ == "__main__":
    main() 