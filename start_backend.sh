#!/bin/bash

echo "🚀 Starting AI Image Generator Backend..."
echo "=================================="

# Check if environment variables are set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not set"
    echo "   Set it with: export OPENAI_API_KEY='your-key-here'"
fi

if [ -z "$SERPAPI_KEY" ]; then
    echo "⚠️  Warning: SERPAPI_KEY not set"
    echo "   Set it with: export SERPAPI_KEY='your-key-here'"
fi

echo ""
echo "📖 API Documentation will be available at: http://localhost:8000/docs"
echo "🎯 Health Check: http://localhost:8000/health"
echo "🌐 Backend API: http://localhost:8000"
echo ""

# Start the server
python3 api_server.py 