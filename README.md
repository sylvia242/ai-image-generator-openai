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

### Basic Usage
```bash
python ai_image_generator.py path/to/your/image.jpg
```

### Advanced Usage
```bash
python ai_image_generator.py path/to/your/image.jpg \
  --style "scandinavian" \
  --instructions "Focus on sustainable materials and natural lighting" \
  --type "living room redesign" \
  --output "my_design_results.json"
```

### Command Line Options

- `image_path`: Path to the image file to analyze (required)
- `--api-key`: OpenAI API key (optional if set as environment variable)
- `--style`: Design style (default: "modern")
- `--instructions`: Custom design instructions (optional)
- `--type`: Type of design project (default: "interior redesign")
- `--output`: Output JSON file name (default: "design_results.json")
- `--no-save`: Don't save results to file (optional)

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