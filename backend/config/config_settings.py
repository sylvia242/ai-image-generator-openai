"""
Configuration file for AI Image Generator
"""
import os

# OpenAI API Key - You can set this in several ways:
# 1. Set as environment variable: export OPENAI_API_KEY="your_key_here"
# 2. Create a .env file with: OPENAI_API_KEY=your_key_here
# 3. Uncomment and set the API_KEY variable below

# OpenAI API Key - Set via environment variable OPENAI_API_KEY
# SerpAPI Key for product search - Set via environment variable SERPAPI_KEY

def get_api_key():
    """Get OpenAI API key from environment variable"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set")
    return api_key

def get_serpapi_key():
    """Get SerpAPI key from environment variable"""
    serpapi_key = os.getenv('SERPAPI_KEY')
    if not serpapi_key:
        print("⚠️  Warning: SERPAPI_KEY environment variable not set")
    return serpapi_key 