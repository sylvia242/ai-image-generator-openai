"""
Configuration module for AI Image Generator
"""
import os
import sys
from pathlib import Path

# Add parent directory to path to import config_template
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

def get_api_key():
    """Get OpenAI API key from various sources"""
    # Try environment variable first
    api_key = os.getenv('OPENAI_API_KEY')
    
    # If not found in environment, try importing from config_template
    if not api_key:
        try:
            from config_template import get_api_key as template_get_api_key
            api_key = template_get_api_key()
        except (ImportError, AttributeError):
            pass
    
    return api_key
