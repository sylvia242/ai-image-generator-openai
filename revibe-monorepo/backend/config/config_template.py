"""
Configuration template for AI Image Generator
Copy this file to config.py and add your API key
"""
import os

# OpenAI API Key - You can set this in several ways:
# 1. Set as environment variable: export OPENAI_API_KEY="your_key_here"
# 2. Create a .env file with: OPENAI_API_KEY=your_key_here
# 3. Uncomment and set the API_KEY variable below

# Uncomment the line below and add your actual API key:
# API_KEY = "your_openai_api_key_here"

def get_api_key():
    """Get OpenAI API key from various sources"""
    # Try environment variable first
    api_key = os.getenv('OPENAI_API_KEY')
    
    # If not found in environment, try the hardcoded key
    if not api_key and 'API_KEY' in globals():
        api_key = API_KEY
    
    return api_key 