#!/usr/bin/env python3
"""
Performance Tracking Test
Demonstrates the performance tracking functionality for the AI design pipeline
"""

import os
import sys
import time
sys.path.append('.')

from src.core.real_products_pathway import RealProductsPathway
from config.config_settings import get_api_key, get_serpapi_key
from src.utils.session_manager import SessionManager

def test_performance_tracking():
    """Test optimized parallel product search performance"""
    
    # Get API keys
    openai_key = get_api_key()
    serpapi_key = get_serpapi_key()
    
    if not openai_key:
        print("❌ OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        return
    
    if not serpapi_key:
        print("❌ SerpAPI key not found. Please set SERPAPI_KEY environment variable.")
        return
    
    print("🧪 Testing Performance Tracking")
    print("=" * 50)
    
    # Initialize SessionManager for organized output
    session = SessionManager()
    print(f"📁 Session ID: {session.session_id}")
    
    # Initialize pathway (default is False, but explicit for clarity)
    pathway = RealProductsPathway(openai_key, fast_mode=False)
    
    # Test parameters
    design_style = "modern"
    custom_instructions = "Create a clean, minimalist design"
    design_type = "interior redesign"
    
    # Use the user's actual image
    sample_image_path = "/Users/sylviaschumacher/Desktop/Screenshot 2025-07-29 at 7.36.09 PM.png"
    
    if not os.path.exists(sample_image_path):
        print(f"❌ Sample image not found: {sample_image_path}")
        print("Please provide a valid image path for testing")
        return
    
    print(f"📸 Using sample image: {sample_image_path}")
    print(f"🎨 Design style: {design_style}")
    print(f"⚡ Fast mode: False (for detailed tracking)")
    print()
    
    try:
        # Generate design with performance tracking
        print("🚀 Starting design generation with performance tracking...")
        print()
        
        results = pathway.generate_design_with_real_products(
            image_path=sample_image_path,
            design_style=design_style,
            custom_instructions=custom_instructions,
            design_type=design_type,
            serpapi_key=serpapi_key,
            fast_mode=False  # Use detailed mode for better tracking
        )
        
        if results and results.get('success'):
            print("\n✅ Design generation completed successfully!")
            print(f"📊 Performance data included in results")
            
            # Show session information
            if 'session_id' in results:
                print(f"\n📁 Session Information:")
                print(f"   🆔 Session ID: {results['session_id']}")
                print(f"   📂 Session Path: {results['session_path']}")
            
            # Show performance summary
            if 'total_duration' in results:
                print(f"\n📈 Performance Summary:")
                print(f"   ⏱️ Total duration: {results['total_duration']:.2f}s")
                
                if 'step_durations' in results:
                    print(f"   📋 Step breakdown:")
                    for step_name, duration in results['step_durations'].items():
                        print(f"      • {step_name}: {duration:.2f}s")
                
                if 'performance_report' in results:
                    print(f"   📄 Detailed report: {results['performance_report']}")
            
            print(f"\n📦 Products found: {results.get('products_used', 0)}")
            print(f"🎨 Final design: {results.get('final_design', 'N/A')}")
            
            # Create latest symlink for easy access
            session.create_latest_symlink()
            print(f"🔗 Latest session symlink created: output/sessions/latest")
            
        else:
            print("❌ Design generation failed")
            if results and 'error' in results:
                print(f"   Error: {results['error']}")
    
    except Exception as e:
        print(f"❌ Error during performance tracking test: {e}")

def test_fast_mode_performance():
    """Test performance tracking in fast mode"""
    
    # Get API keys
    openai_key = get_api_key()
    serpapi_key = get_serpapi_key()
    
    if not openai_key or not serpapi_key:
        print("❌ API keys not found")
        return
    
    print("\n" + "=" * 50)
    print("⚡ Testing Fast Mode Performance")
    print("=" * 50)
    
    # Initialize pathway with fast mode enabled
    pathway = RealProductsPathway(openai_key, fast_mode=True)
    
    # Test parameters
    design_style = "modern"
    custom_instructions = "Create a clean, minimalist design"
    design_type = "interior redesign"
    
    # Use the user's actual image
    sample_image_path = "/Users/sylviaschumacher/Desktop/Screenshot 2025-07-29 at 7.36.09 PM.png"
    
    if not os.path.exists(sample_image_path):
        print(f"❌ Sample image not found: {sample_image_path}")
        return
    
    print(f"📸 Using sample image: {sample_image_path}")
    print(f"🎨 Design style: {design_style}")
    print(f"⚡ Fast mode: True (for speed optimization)")
    print()
    
    try:
        # Generate design with performance tracking
        print("🚀 Starting fast mode design generation...")
        print()
        
        results = pathway.generate_design_with_real_products(
            image_path=sample_image_path,
            design_style=design_style,
            custom_instructions=custom_instructions,
            design_type=design_type,
            serpapi_key=serpapi_key,
            fast_mode=True  # Use fast mode
        )
        
        if results and results.get('success'):
            print("\n✅ Fast mode design generation completed!")
            
            # Show performance comparison
            if 'total_duration' in results:
                print(f"\n📈 Fast Mode Performance:")
                print(f"   ⏱️ Total duration: {results['total_duration']:.2f}s")
                
                if 'step_durations' in results:
                    print(f"   📋 Step breakdown:")
                    for step_name, duration in results['step_durations'].items():
                        print(f"      • {step_name}: {duration:.2f}s")
            
            print(f"\n📦 Products found: {results.get('products_used', 0)}")
            
        else:
            print("❌ Fast mode design generation failed")
            if results and 'error' in results:
                print(f"   Error: {results['error']}")
    
    except Exception as e:
        print(f"❌ Error during fast mode test: {e}")

def show_performance_reports():
    """Show available performance reports"""
    
    print("\n" + "=" * 50)
    print("📊 Available Performance Reports")
    print("=" * 50)
    
    performance_dir = "performance_tracking"
    if not os.path.exists(performance_dir):
        print("❌ No performance tracking directory found")
        return
    
    reports = []
    for filename in os.listdir(performance_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(performance_dir, filename)
            stat = os.stat(filepath)
            reports.append({
                "filename": filename,
                "path": filepath,
                "created": time.ctime(stat.st_ctime),
                "size": stat.st_size
            })
    
    if not reports:
        print("📭 No performance reports found")
        return
    
    # Sort by creation time (newest first)
    reports.sort(key=lambda x: x['created'], reverse=True)
    
    print(f"📋 Found {len(reports)} performance reports:")
    for i, report in enumerate(reports[:5], 1):  # Show latest 5
        print(f"   {i}. {report['filename']}")
        print(f"      Created: {report['created']}")
        print(f"      Size: {report['size']} bytes")
        print()

if __name__ == "__main__":
    print("🧪 Performance Tracking Test Suite")
    print("Testing comprehensive performance monitoring")
    print()
    
    # Test regular performance tracking
    test_performance_tracking()
    
    # Test fast mode performance
    test_fast_mode_performance()
    
    # Show available reports
    show_performance_reports() 