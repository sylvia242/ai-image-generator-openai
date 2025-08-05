#!/bin/bash
# Quick run script for examples

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 AI Image Generation - Quick Examples${NC}"
echo "=========================================="

# Check if API keys are set
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${RED}❌ OPENAI_API_KEY not set${NC}"
    echo "Please set your OpenAI API key:"
    echo "export OPENAI_API_KEY='your_key_here'"
    exit 1
fi

if [ -z "$SERPAPI_KEY" ]; then
    echo -e "${YELLOW}⚠️  SERPAPI_KEY not set (real products pathway will fail)${NC}"
fi

# Function to run example
run_example() {
    local script=$1
    local description=$2
    
    echo -e "\n${GREEN}🎨 Running: $description${NC}"
    echo "Script: $script"
    echo "----------------------------------------"
    
    if python3 "$script"; then
        echo -e "${GREEN}✅ $description completed successfully!${NC}"
    else
        echo -e "${RED}❌ $description failed${NC}"
        return 1
    fi
}

# Main examples
echo -e "\n${BLUE}📚 Available Examples:${NC}"
echo "1. Real products pathway (SerpAPI products)"
echo "2. Real products pathway - FAST MODE"
echo "3. Performance tracking"
echo "4. All examples"

read -p "Choose an example (1-4): " choice

case $choice in
    1)
        if [ -z "$SERPAPI_KEY" ]; then
            echo -e "${RED}❌ SERPAPI_KEY required for real products pathway${NC}"
            exit 1
        fi
        run_example "examples/example_real_products.py" "Real Products Pathway"
        ;;
    2)
        if [ -z "$SERPAPI_KEY" ]; then
            echo -e "${RED}❌ SERPAPI_KEY required for real products pathway${NC}"
            exit 1
        fi
        echo -e "\n${YELLOW}⚡ Running in FAST MODE...${NC}"
        # Create a temporary fast mode script
        cat > /tmp/fast_mode_example.py << 'EOF'
#!/usr/bin/env python3
import sys
import os
sys.path.append('.')

from src.core.real_products_pathway import RealProductsPathway
from config.config_settings import get_api_key, get_serpapi_key

def main():
    openai_key = get_api_key()
    serpapi_key = get_serpapi_key()
    
    if not openai_key or not serpapi_key:
        print("❌ API keys required")
        return
    
    pathway = RealProductsPathway(openai_key, fast_mode=True)
    
    # Use a sample image or prompt user
    image_path = "/Users/sylviaschumacher/Desktop/Screenshot 2025-07-29 at 7.36.09 PM.png"
    
    if not os.path.exists(image_path):
        print(f"❌ Sample image not found: {image_path}")
        print("Please update the image_path in the script")
        return
    
    print("⚡ FAST MODE - Real Products Pathway")
    print("=" * 50)
    
    results = pathway.generate_design_with_real_products(
        image_path=image_path,
        design_style="modern",
        custom_instructions="Add clean lines and contemporary styling",
        design_type="interior redesign",
        serpapi_key=serpapi_key,
        fast_mode=True
    )
    
    if results and results.get('success'):
        print("✅ Fast mode completed successfully!")
        print(f"📁 Session: {results.get('session_id', 'N/A')}")
    else:
        print("❌ Fast mode failed")

if __name__ == "__main__":
    main()
EOF
        
        python3 /tmp/fast_mode_example.py
        rm /tmp/fast_mode_example.py
        ;;
    3)
        run_example "examples/performance/test_performance_tracking.py" "Performance Tracking"
        ;;
    4)
        echo -e "\n${BLUE}🔄 Running all examples...${NC}"
        
        run_example "examples/example_real_products.py" "Real Products Pathway"
        echo -e "\n${YELLOW}⚡ Running FAST MODE example...${NC}"
        # Run fast mode example here
        run_example "examples/performance/test_performance_tracking.py" "Performance Tracking"
        
        echo -e "\n${GREEN}🎉 All examples completed!${NC}"
        ;;
    *)
        echo -e "${RED}❌ Invalid choice${NC}"
        exit 1
        ;;
esac

echo -e "\n${BLUE}📁 Check output/sessions/latest for results${NC}" 