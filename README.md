# AI Image Generator

This Python script is based on the prompt structure from the HostLux AI Interior Design Platform. It uses OpenAI's GPT-4 Vision to analyze uploaded images and generate detailed design recommendations and transformations.

## Features

- 🖼️ **Image Analysis**: Upload any image and get detailed AI analysis
- 🎨 **Design Recommendations**: Get specific design transformation suggestions
- 🎯 **Multiple Styles**: Support for various design styles (modern, rustic, minimalist, etc.)
- 📊 **Structured Output**: Results in both human-readable format and JSON
- ⚙️ **Customizable**: Add custom instructions and design preferences

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup OpenAI API Key**:
   - Go to [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a new API key
   - Choose one of these setup methods:
   
   **Method 1: Config File (Easiest)**
   ```bash
   cp config_template.py config.py
   # Edit config.py and uncomment/set the API_KEY variable
   ```
   
   **Method 2: Environment Variable**
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

## Usage

### Quick Start
```bash
# Run examples interactively
./scripts/run_examples.sh

# Or run specific examples
python3 examples/example_real_products.py
```

### Main Examples

#### **Real Products Pathway (SerpAPI products)**
```bash
python3 examples/example_real_products.py
```

#### **Performance Tracking**
```bash
python3 examples/performance/test_performance_tracking.py
```

### API Server
```bash
python3 api_server.py
```

### Debug Image Generation
```bash
python3 tests/test_image_generation_debug.py
```

### Fast Mode
```bash
# Quick processing with reduced quality
python3 src/core/ai_image_generator.py your_image.jpg --fast

# Full quality processing (default)
python3 src/core/ai_image_generator.py your_image.jpg
```

See [FAST_MODE_GUIDE.md](FAST_MODE_GUIDE.md) for detailed information about fast mode.

### Supported Design Styles

- modern
- scandinavian
- minimalist
- rustic
- industrial
- bohemian
- traditional
- contemporary
- farmhouse
- mid-century

### Example Output

The script provides:

1. **Current State Analysis**: What the AI sees in your image
2. **Design Concept**: Overall vision and style recommendations
3. **Specific Recommendations**: Detailed suggestions with priorities
4. **Transformation Summary**: Expected impact and changes

## Original Prompt Source

This script is based on the AI prompts found in the HostLux AI Interior Design Platform repository:
- Repository: https://github.com/MarvinFernie/fern-project-new-project-8370a695.git
- Original prompt structure from: `src/app/api/generate-design/route.ts`

The original platform was designed for Airbnb interior design optimization, but this script generalizes the concept for any image analysis and design recommendations.

## Requirements

- Python 3.7+
- Valid OpenAI API key
- Internet connection for API calls
- Supported image formats: JPG, JPEG, PNG, GIF, WebP

## Error Handling

The script includes comprehensive error handling for:
- Invalid image files
- Missing API keys
- Network connectivity issues
- API response errors
- JSON parsing errors

## License

This script is based on the HostLux AI platform structure and is provided for educational and personal use. 