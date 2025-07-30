#!/bin/bash

# Template for starting the backend with API keys
# Copy this file to start_backend_with_keys.sh and add your actual API keys

# Set API keys (replace with your actual keys)
export OPENAI_API_KEY="your-openai-api-key-here"
export SERPAPI_KEY="your-serpapi-key-here"

echo "🚀 Starting AI Image Generator Backend with API keys..."
echo "📖 API Documentation: http://localhost:8000/docs"
echo "🎯 Health Check: http://localhost:8000/health"

# Start the server
python3 api_server.py 