# Performance Tracking

This directory contains performance tracking functionality for the AI design pipeline.

## Overview

The performance tracking system captures detailed timing information for each step in the AI design generation process:

1. **Vision Analysis** - GPT-4 Vision image analysis
2. **Product Search** - SerpAPI Google Shopping product search
3. **Composite Creation** - Creating composite layout with base image and products
4. **Image Generation** - GPT Image 1 final design generation

## Files

- `performance_tracker.py` - Core performance tracking module
- `README.md` - This documentation file

## Usage

### Basic Usage

```python
from performance_tracking.performance_tracker import create_tracker, track_vision_analysis

# Create a tracker
tracker = create_tracker()
tracker.start_pipeline(fast_mode=False)

# Track individual steps
with track_vision_analysis(tracker):
    # Your vision analysis code here
    pass

# End tracking
tracker.end_pipeline(success=True, product_count=5)
tracker.save_performance_report()
tracker.print_summary()
```

### Integration with Real Products Pathway

The performance tracking is automatically integrated into the `RealProductsPathway` class. Each design generation will:

1. Create a performance tracker
2. Track each step with detailed timing
3. Save a JSON performance report
4. Include performance data in the response

### Performance Report Structure

```json
{
  "session_id": "20250730_143022",
  "total_duration": 45.23,
  "fast_mode": false,
  "success": true,
  "product_count": 6,
  "timestamp": "2025-07-30T14:30:22.123456",
  "steps": [
    {
      "step_name": "Vision Analysis",
      "start_time": 1698678622.123,
      "end_time": 1698678645.456,
      "duration": 23.333,
      "success": true,
      "error_message": null,
      "additional_data": {
        "design_style": "modern",
        "design_type": "interior redesign"
      }
    }
  ]
}
```

## Step Breakdown

### Vision Analysis
- **Purpose**: Analyze uploaded room image with GPT-4 Vision
- **Metrics**: Duration, success/failure, design style parameters
- **Optimizations**: Fast mode uses `gpt-4o-mini` instead of `gpt-4o`

### Product Search
- **Purpose**: Search for real products using SerpAPI Google Shopping
- **Metrics**: Duration, number of products found, parallel worker count
- **Optimizations**: 8 parallel workers, HTTP session reuse

### Composite Creation
- **Purpose**: Create composite layout with base image and product thumbnails
- **Metrics**: Duration, product count, image processing time
- **Optimizations**: Fast mode uses smaller image sizes

### Image Generation
- **Purpose**: Use GPT Image 1 to generate final design
- **Metrics**: Duration, image generation time, quality settings
- **Optimizations**: Fast mode uses smaller output size

## Performance Optimizations

### Fast Mode
- Uses `gpt-4o-mini` for vision analysis
- Limits product searches to 3 types
- Uses smaller image sizes for composite and generation
- Reduces max tokens and sets temperature to 0

### Parallel Processing
- Up to 8 concurrent SerpAPI searches
- HTTP session reuse for connection pooling
- Automatic retry mechanism for failed requests

## Monitoring

### Real-time Output
Performance tracking provides real-time console output:
```
🚀 Performance tracking started (Session: 20250730_143022)
   ⚡ Fast mode: False
   🔍 Starting step: Vision Analysis
   ✅ Completed step: Vision Analysis (23.33s)
   🔍 Starting step: Product Search
   ✅ Completed step: Product Search (12.45s)
```

### Summary Reports
After completion, a detailed summary is printed:
```
============================================================
📊 PERFORMANCE SUMMARY
============================================================
Session ID: 20250730_143022
Fast Mode: False
Success: True
Products Found: 6
Total Duration: 45.23s

📋 Step Breakdown:
   ✅ Vision Analysis: 23.33s
   ✅ Product Search: 12.45s
   ✅ Composite Creation: 2.34s
   ✅ Image Generation: 7.11s

📈 Step Percentages:
   Vision Analysis: 51.6%
   Product Search: 27.5%
   Composite Creation: 5.2%
   Image Generation: 15.7%
```

## API Integration

The performance data is automatically included in API responses:

```json
{
  "success": true,
  "data": {
    "final_design": "path/to/final/image.png",
    "products_info": [...],
    "performance_report": "performance_tracking/performance_report_20250730_143022.json",
    "total_duration": 45.23,
    "step_durations": {
      "Vision Analysis": 23.33,
      "Product Search": 12.45,
      "Composite Creation": 2.34,
      "Image Generation": 7.11
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **Missing performance reports**: Check that the `performance_tracking` directory exists and is writable
2. **Incomplete tracking**: Ensure all steps are wrapped in the appropriate tracking context managers
3. **Memory issues**: Large images may cause memory problems during composite creation

### Debug Mode

To enable detailed debugging, set the log level:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

- **Performance alerts**: Set thresholds for step durations
- **Historical analysis**: Compare performance across multiple runs
- **Resource monitoring**: Track CPU and memory usage
- **Bottleneck identification**: Automatic identification of slowest steps 