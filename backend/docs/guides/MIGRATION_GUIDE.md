# 📁 Migration Guide: New File Organization

## 🎯 **Overview**

This guide helps you migrate from the old scattered file structure to the new organized session-based system.

## 📋 **What Changed**

### **Before (Old Structure)**
```
ai_image_generation_clean/
├── serpapi_product_*.jpg          # Scattered in root
├── composite_layout_*.png         # Scattered in root
├── design_results.json            # Scattered in root
├── test_output/                   # Mixed outputs
├── serpapi_products/             # Mixed sessions
└── shopping_lists/               # Mixed outputs
```

### **After (New Structure)**
```
ai_image_generation_clean/
├── output/
│   ├── sessions/
│   │   └── YYYY-MM-DD_HH-MM-SS/
│   │       ├── products/          # Downloaded images
│   │       ├── composites/        # Layout images
│   │       ├── final_designs/     # Generated designs
│   │       ├── analysis/          # Analysis results
│   │       ├── shopping_lists/    # Shopping lists
│   │       └── debug/             # Debug outputs
│   ├── temp/                      # Temporary files
│   └── archive/                   # Archived results
└── scripts/                       # Management scripts
```

## 🔧 **Migration Steps**

### **Step 1: Update Your Code**

Replace direct file path generation with SessionManager:

```python
# OLD WAY
import os
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = "test_output"
final_image_path = os.path.join(output_dir, f"real_products_overlay_design_{timestamp}.png")

# NEW WAY
from src.utils.session_manager import SessionManager

session = SessionManager()
final_image_path = session.save_file('final_designs', f"real_products_overlay_design_{timestamp}.png", 
                                   source_path=temp_image_path)
```

### **Step 2: Update File Paths**

#### **Product Images**
```python
# OLD
product_path = f"serpapi_product_{product_name}_{timestamp}.jpg"

# NEW
product_path = session.save_file('products', f"{product_name}_{timestamp}.jpg", 
                                source_path=downloaded_path)
```

#### **Composite Layouts**
```python
# OLD
composite_path = os.path.join("test_output", f"composite_layout_{timestamp}.png")

# NEW
composite_path = session.save_file('composites', f"composite_layout_{timestamp}.png", 
                                 source_path=temp_composite_path)
```

#### **Analysis Results**
```python
# OLD
analysis_path = "design_results.json"

# NEW
analysis_path = session.save_file('analysis', 'design_results.json', 
                                content=json.dumps(analysis_data))
```

### **Step 3: Update Existing Classes**

#### **RealProductsPathway Class**
```python
# Add to __init__
from src.utils.session_manager import SessionManager

class RealProductsPathway:
    def __init__(self, api_key, serpapi_key, fast_mode=False):
        # ... existing code ...
        self.session = SessionManager()
    
    def create_composite_layout(self, base_image_path, products):
        # ... existing code ...
        
        # Save composite
        composite_path = self.session.save_file('composites', 
                                             f"composite_layout_{timestamp}.png",
                                             source_path=temp_composite_path)
        return composite_path
    
    def overlay_products_with_gpt_image_1(self, composite_image_path, prompt):
        # ... existing code ...
        
        # Save final design
        final_path = self.session.save_file('final_designs',
                                          f"real_products_overlay_design_{timestamp}.png",
                                          source_path=temp_final_path)
        return final_path
```

#### **Shopping List Generator**
```python
# Add to shopping list generation
def generate_shopping_list(self, analysis_results):
    # ... existing code ...
    
    # Save shopping list
    shopping_list_path = self.session.save_file('shopping_lists',
                                              f"shopping_list_{timestamp}.html",
                                              content=html_content)
    return shopping_list_path
```

### **Step 4: Update Test Scripts**

#### **Performance Tracking Script**
```python
# examples/test_performance_tracking.py
from src.utils.session_manager import SessionManager

def main():
    session = SessionManager()
    
    # Your existing code, but use session.save_file() for outputs
    # session.save_file('debug', 'performance_log.txt', content=log_content)
    # session.save_file('analysis', 'analysis_results.json', content=json.dumps(results))
```

## 🚀 **Integration Examples**

### **Complete Integration Example**
```python
#!/usr/bin/env python3
"""
Example of using SessionManager in your scripts
"""

import sys
import os
sys.path.append('src')

from src.utils.session_manager import SessionManager
from src.core.real_products_pathway import RealProductsPathway
from config.config_settings import get_api_key, get_serpapi_key

def main():
    # Create session manager
    session = SessionManager()
    print(f"📁 Session ID: {session.session_id}")
    
    # Initialize pathway with session
    api_key = get_api_key()
    serpapi_key = get_serpapi_key()
    
    pathway = RealProductsPathway(api_key, serpapi_key, fast_mode=True)
    pathway.session = session  # Use the same session
    
    # Run your analysis
    image_path = "/path/to/your/image.jpg"
    
    # Analysis will be saved to session/analysis/
    analysis_results = pathway.analyze_room_image(image_path)
    
    # Products will be saved to session/products/
    products = pathway.search_products(analysis_results)
    
    # Composite will be saved to session/composites/
    composite_path = pathway.create_composite_layout(image_path, products)
    
    # Final design will be saved to session/final_designs/
    final_design_path = pathway.overlay_products_with_gpt_image_1(composite_path, prompt)
    
    # Shopping list will be saved to session/shopping_lists/
    shopping_list_path = pathway.generate_shopping_list(analysis_results)
    
    print(f"✅ All outputs saved to session: {session.session_id}")
    print(f"📁 Session path: {session.session_path}")
    
    # Create latest symlink for easy access
    session.create_latest_symlink()

if __name__ == "__main__":
    main()
```

## 🧹 **Cleanup and Maintenance**

### **Automatic Cleanup**
```bash
# Clean old sessions (older than 30 days)
./scripts/cleanup.sh

# Dry run to see what would be cleaned
./scripts/cleanup.sh -n -v

# Clean sessions older than 7 days
./scripts/cleanup.sh -d 7
```

### **Manual Session Management**
```python
from src.utils.session_manager import SessionManager

# Create session
session = SessionManager()

# Archive important session
session.archive_session("bohemian_living_room_design")

# Clean up temp files
session.cleanup_temp_files()

# Clean old sessions (30+ days)
session.cleanup_old_sessions(days=30)
```

## 📊 **Benefits After Migration**

### **✅ Organization**
- **Predictable paths** - Always know where files are saved
- **Session isolation** - Each run is self-contained
- **Easy navigation** - Clear folder structure

### **✅ Maintenance**
- **Automatic cleanup** - Old sessions removed automatically
- **Easy backups** - Archive important sessions
- **Version control friendly** - Outputs don't clutter git

### **✅ Debugging**
- **Debug outputs organized** - All debug files in session/debug/
- **Session tracking** - Easy to find specific run outputs
- **Latest symlink** - Quick access to most recent session

## 🔍 **Troubleshooting**

### **Common Issues**

#### **File Not Found Errors**
```python
# Make sure directories exist
session = SessionManager()
# Directories are created automatically
```

#### **Permission Errors**
```bash
# Make scripts executable
chmod +x scripts/*.sh
```

#### **Session Manager Import Error**
```python
# Add src to path
import sys
sys.path.append('src')
from src.utils.session_manager import SessionManager
```

### **Debugging Tips**

#### **Check Session Structure**
```python
session = SessionManager()
print("Session Info:", session.get_session_info())
```

#### **List Session Contents**
```bash
# List current session
ls -la output/sessions/latest/

# List all sessions
ls -la output/sessions/
```

## 🎯 **Next Steps**

1. **Update your main scripts** to use SessionManager
2. **Test with a small example** to ensure everything works
3. **Run cleanup script** to manage old files
4. **Archive important results** using the archive system

## 📞 **Need Help?**

- Check the `FILE_ORGANIZATION_PROPOSAL.md` for detailed structure
- Run `./scripts/setup.sh -v` to verify your setup
- Use `./scripts/cleanup.sh -n` to see what would be cleaned
- Test the session manager: `python3 src/utils/session_manager.py`

This new structure will make your project much more maintainable and organized! 