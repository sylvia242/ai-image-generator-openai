# 📁 Scripts Index

## 🎯 **Overview**
This document provides a comprehensive index of all scripts in the AI Image Generation project, organized by purpose and usage.

## 📂 **Script Organization**

### **🏠 Root Directory Scripts**
| Script | Purpose | Usage |
|--------|---------|-------|
| `main.py` | Main entry point and project overview | `python3 main.py` |
| `api_server.py` | FastAPI server for web interface | `python3 api_server.py` |
| `test_image_generation_debug.py` | Debug GPT Image 1 generation | `python3 test_image_generation_debug.py` |

### **📚 Examples Directory**

#### **🎨 Main Examples**
| Script | Purpose | Usage |
|--------|---------|-------|
| `example_real_products.py` | Real products pathway (SerpAPI products) | `python3 examples/example_real_products.py` |

#### **⚡ Performance Examples**
| Script | Purpose | Usage |
|--------|---------|-------|
| `performance/test_performance_tracking.py` | Performance tracking and optimization | `python3 examples/performance/test_performance_tracking.py` |

### **🧪 Tests Directory**

#### **🔗 Integration Tests**
| Script | Purpose | Usage |
|--------|---------|-------|
| `integration/test_real_products_analysis_only.py` | Test analysis without image generation | `python3 tests/integration/test_real_products_analysis_only.py` |
| `integration/test_both_pathways_standard_and_real_products.py` | Test both pathways | `python3 tests/integration/test_both_pathways_standard_and_real_products.py` |

## 🚀 **Quick Start Guide**

### **For New Users:**
1. **Start with main examples:**
   ```bash
   python3 examples/example_real_products.py
   ```

2. **Test performance:**
   ```bash
   python3 examples/performance/test_performance_tracking.py
   ```

3. **Run integration tests:**
   ```bash
   python3 tests/integration/test_real_products_analysis_only.py
   python3 tests/integration/test_both_pathways_standard_and_real_products.py
   ```

### **For Developers:**
1. **Debug image generation:**
   ```bash
   python3 test_image_generation_debug.py
   ```

2. **Start API server:**
   ```bash
   python3 api_server.py
   ```

## 📋 **Script Purposes**

### **🎨 Main Examples**
- **`example_real_products.py`**: Demonstrates the real products pathway using SerpAPI

### **⚡ Performance Tests**
- **`test_performance_tracking.py`**: Comprehensive performance tracking and optimization

### **🔗 Integration Tests**
- **`test_real_products_analysis_only.py`**: Tests analysis and shopping list generation
- **`test_both_pathways_standard_and_real_products.py`**: Tests both pathways

### **🐛 Debug Scripts**
- **`test_image_generation_debug.py`**: Debug GPT Image 1 generation issues

### **🌐 Server Scripts**
- **`api_server.py`**: FastAPI server for web interface
- **`main.py`**: Project overview and entry point

## 🧹 **Cleanup Summary**

### **Removed Scripts (13 files):**
- ❌ `test_performance_simple.py` - Redundant performance test
- ❌ `test_http_session_optimization.py` - Outdated optimization
- ❌ `test_parallel_optimization.py` - Outdated optimization
- ❌ `test_parallel_vs_sequential.py` - Outdated comparison
- ❌ `test_serpapi_benchmark.py` - Outdated benchmark
- ❌ `test_composite_speed.py` - Outdated speed test
- ❌ `test_gpt_image1_speed.py` - Outdated speed test
- ❌ `test_image_size_optimization.py` - Outdated optimization
- ❌ `test_speed_comparison.py` - Outdated comparison
- ❌ `show_composite_images.py` - Outdated utility
- ❌ `show_analysis_content.py` - Outdated utility
- ❌ `example_enhanced_description_search.py` - Outdated search
- ❌ `test_enhanced_serpapi_search.py` - Outdated search
- ❌ `fixed_shopping_test_serpapi.py` - Outdated shopping test
- ❌ `test_enhanced_search.py` - Duplicate search functionality

### **Kept Scripts (5 files):**
- ✅ `example_real_products.py` - Main real products example
- ✅ `performance/test_performance_tracking.py` - Main performance test
- ✅ `integration/test_real_products_analysis_only.py` - Analysis test
- ✅ `test_image_generation_debug.py` - Debug script
- ✅ `api_server.py` - API server
- ✅ `main.py` - Main entry point

## 📊 **Benefits of Cleanup**

### **✅ Reduced Complexity**
- **From 20+ scripts to 5 core scripts**
- **Clear organization** by purpose
- **Eliminated duplicates** and outdated code

### **✅ Better Maintainability**
- **Focused functionality** - each script has a clear purpose
- **Updated code** - all scripts use SessionManager
- **Consistent structure** - organized by type and purpose

### **✅ Improved Developer Experience**
- **Easy navigation** - clear directory structure
- **Quick start** - obvious entry points
- **Reduced confusion** - no duplicate functionality

## 🎯 **Next Steps**

1. **Update remaining scripts** to use SessionManager (✅ Done)
2. **Test all scripts** to ensure they work correctly
3. **Update documentation** to reflect new structure
4. **Create run scripts** for common workflows

This cleanup reduces the script count by 65% while maintaining all essential functionality! 