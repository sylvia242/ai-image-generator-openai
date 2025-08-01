# ⚡ Fast Mode Guide

## 🎯 **Overview**
Fast mode is a performance optimization feature that trades quality for speed in the AI image generation pipeline. It's designed for quick prototyping and testing when you need faster results.

## 🚀 **How to Enable Fast Mode**

### **Command Line Interface**
```bash
# Enable fast mode for quicker processing
python3 src/core/ai_image_generator.py your_image.jpg --fast

# With additional options
python3 src/core/ai_image_generator.py your_image.jpg --fast --style "modern" --instructions "Add plants"
```

### **API Server**
```bash
# Fast mode is disabled by default, enable via API parameter
curl -X POST "http://localhost:8000/generate-real-products" \
  -F "file=@your_image.jpg" \
  -F "design_style=modern" \
  -F "fast_mode=true"
```

### **Python Code**
```python
from src.core.real_products_pathway import RealProductsPathway

# Initialize with fast mode enabled
pathway = RealProductsPathway(api_key, fast_mode=True)

# Or enable for specific generation
results = pathway.generate_design_with_real_products(
    image_path="your_image.jpg",
    fast_mode=True
)
```

## ⚙️ **What Fast Mode Does**

### **1. Vision Model Optimization**
- **Standard Mode**: Uses `gpt-4o` (highest quality)
- **Fast Mode**: Uses `gpt-4o-mini` (faster, slightly lower quality)

### **2. Token Limits**
- **Standard Mode**: 2048 max tokens, temperature 0.7
- **Fast Mode**: 1024 max tokens, temperature 0 (more deterministic)

### **3. Image Processing**
- **Standard Mode**: Full resolution processing
- **Fast Mode**: Reduced image sizes for faster processing

### **4. Product Search**
- **Standard Mode**: Searches for 8 product types
- **Fast Mode**: Limits to top 3 product types

### **5. Early Exit**
- **Standard Mode**: Processes all products
- **Fast Mode**: Exits early when 3 products are found

### **6. Composite Layout**
- **Standard Mode**: Full quality composite images
- **Fast Mode**: Reduced size composites (768px max vs 1024px)

### **7. Image Generation**
- **Standard Mode**: High fidelity GPT Image 1
- **Fast Mode**: Medium fidelity GPT Image 1

## 📊 **Performance Comparison**

| Aspect | Standard Mode | Fast Mode | Speed Improvement |
|--------|---------------|-----------|-------------------|
| Vision Analysis | ~10-15s | ~5-8s | ~50% faster |
| Product Search | ~30-45s | ~15-25s | ~50% faster |
| Image Generation | ~30-60s | ~20-40s | ~40% faster |
| Total Pipeline | ~70-120s | ~40-73s | ~45% faster |

## 🎯 **When to Use Fast Mode**

### **✅ Use Fast Mode When:**
- **Quick prototyping** - Testing different styles quickly
- **Development** - Debugging and testing
- **Batch processing** - Processing multiple images
- **Limited time** - Need results quickly
- **Testing** - Validating concepts

### **❌ Avoid Fast Mode When:**
- **Final designs** - Need highest quality
- **Client work** - Professional results required
- **Detailed analysis** - Need comprehensive recommendations
- **Complex rooms** - Need thorough product search

## 🔧 **Configuration**

### **Default Behavior**
- **Fast Mode**: `False` (quality over speed)
- **CLI**: `--fast` flag to enable
- **API**: `fast_mode=false` by default

### **Environment Variables**
```bash
# No environment variables needed - controlled via parameters
```

## 📝 **Examples**

### **Quick Test**
```bash
# Fast mode for quick testing
python3 src/core/ai_image_generator.py room.jpg --fast --style "modern"
```

### **Quality Mode**
```bash
# Standard mode for quality results
python3 src/core/ai_image_generator.py room.jpg --style "modern"
```

### **API Usage**
```python
import requests

# Fast mode API call
response = requests.post(
    "http://localhost:8000/generate-real-products",
    files={"file": open("room.jpg", "rb")},
    data={
        "design_style": "modern",
        "fast_mode": "true"  # Enable fast mode
    }
)
```

## 🚨 **Important Notes**

1. **Quality Trade-off**: Fast mode reduces quality for speed
2. **Consistent Results**: Lower temperature (0) makes results more predictable
3. **Limited Products**: Only searches top 3 product types
4. **Smaller Images**: Reduced resolution for faster processing
5. **Early Exit**: Stops when minimum products found

## 🔄 **Switching Between Modes**

### **Development Workflow**
```bash
# 1. Quick testing with fast mode
python3 src/core/ai_image_generator.py test.jpg --fast

# 2. Quality results for final design
python3 src/core/ai_image_generator.py final.jpg
```

### **Batch Processing**
```bash
# Process multiple images quickly
for img in *.jpg; do
    python3 src/core/ai_image_generator.py "$img" --fast
done
```

## 📈 **Monitoring Performance**

The system automatically tracks performance metrics:
- **Total duration**
- **Step-by-step timing**
- **Fast mode impact**

Check the performance reports in the session output for detailed metrics.

---

**💡 Tip**: Use fast mode for development and testing, then switch to standard mode for final results! 