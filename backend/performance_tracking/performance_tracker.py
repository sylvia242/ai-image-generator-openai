#!/usr/bin/env python3
"""
Performance Tracking Module
Captures timing for each processing step in the AI design pipeline
"""

import time
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from contextlib import contextmanager

@dataclass
class StepTiming:
    """Data class for tracking individual step timing"""
    step_name: str
    start_time: float
    end_time: float
    duration: float
    success: bool
    error_message: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None

@dataclass
class PipelineTiming:
    """Data class for tracking entire pipeline timing"""
    session_id: str
    total_start_time: float
    total_end_time: float
    total_duration: float
    steps: list[StepTiming]
    fast_mode: bool
    product_count: int
    success: bool

class PerformanceTracker:
    """Tracks performance metrics for the AI design pipeline"""
    
    def __init__(self, output_dir: str = "performance_tracking"):
        self.output_dir = output_dir
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.total_start_time = None
        self.total_end_time = None
        self.steps = []
        self.current_step = None
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
    
    def start_pipeline(self, fast_mode: bool = False) -> None:
        """Start tracking the entire pipeline"""
        self.total_start_time = time.time()
        self.fast_mode = fast_mode
        print(f"🚀 Performance tracking started (Session: {self.session_id})")
        print(f"   ⚡ Fast mode: {fast_mode}")
    
    def end_pipeline(self, success: bool = True, product_count: int = 0) -> None:
        """End tracking the entire pipeline"""
        self.total_end_time = time.time()
        self.total_duration = self.total_end_time - self.total_start_time
        self.success = success
        self.product_count = product_count
        
        print(f"🏁 Performance tracking completed")
        print(f"   ⏱️ Total duration: {self.total_duration:.2f}s")
        print(f"   📦 Products found: {product_count}")
        print(f"   ✅ Success: {success}")
    
    @contextmanager
    def track_step(self, step_name: str, additional_data: Optional[Dict[str, Any]] = None):
        """Context manager for tracking individual steps"""
        step = StepTiming(
            step_name=step_name,
            start_time=time.time(),
            end_time=0,
            duration=0,
            success=False,
            additional_data=additional_data
        )
        
        self.current_step = step
        print(f"   🔍 Starting step: {step_name}")
        
        try:
            yield step
            step.success = True
        except Exception as e:
            step.error_message = str(e)
            step.success = False
            print(f"   ❌ Step failed: {step_name} - {e}")
            raise
        finally:
            step.end_time = time.time()
            step.duration = step.end_time - step.start_time
            self.steps.append(step)
            
            status = "✅" if step.success else "❌"
            print(f"   {status} Completed step: {step_name} ({step.duration:.2f}s)")
    
    def get_step_summary(self) -> Dict[str, Any]:
        """Get a summary of all step timings"""
        summary = {
            "session_id": self.session_id,
            "total_duration": self.total_duration,
            "fast_mode": self.fast_mode,
            "success": self.success,
            "product_count": self.product_count,
            "steps": []
        }
        
        for step in self.steps:
            step_data = asdict(step)
            summary["steps"].append(step_data)
        
        return summary
    
    def save_performance_report(self) -> str:
        """Save performance report to JSON file"""
        if not self.total_start_time:
            raise ValueError("Pipeline not started")
        
        report = self.get_step_summary()
        
        # Add timestamp
        report["timestamp"] = datetime.now().isoformat()
        
        # Create filename
        filename = f"performance_report_{self.session_id}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📊 Performance report saved: {filepath}")
        return filepath
    
    def print_summary(self) -> None:
        """Print a formatted summary of performance metrics"""
        if not self.total_start_time:
            print("❌ No performance data available")
            return
        
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE SUMMARY")
        print("=" * 60)
        
        print(f"Session ID: {self.session_id}")
        print(f"Fast Mode: {self.fast_mode}")
        print(f"Success: {self.success}")
        print(f"Products Found: {self.product_count}")
        print(f"Total Duration: {self.total_duration:.2f}s")
        
        print(f"\n📋 Step Breakdown:")
        for step in self.steps:
            status = "✅" if step.success else "❌"
            print(f"   {status} {step.step_name}: {step.duration:.2f}s")
            if step.error_message:
                print(f"      Error: {step.error_message}")
        
        # Calculate step percentages
        if self.total_duration > 0:
            print(f"\n📈 Step Percentages:")
            for step in self.steps:
                percentage = (step.duration / self.total_duration) * 100
                print(f"   {step.step_name}: {percentage:.1f}%")
    
    def get_step_duration(self, step_name: str) -> Optional[float]:
        """Get duration for a specific step"""
        for step in self.steps:
            if step.step_name == step_name:
                return step.duration
        return None
    
    def get_total_duration(self) -> float:
        """Get total pipeline duration"""
        if self.total_start_time and self.total_end_time:
            return self.total_end_time - self.total_start_time
        return 0.0

# Convenience functions for easy integration
def create_tracker() -> PerformanceTracker:
    """Create a new performance tracker instance"""
    return PerformanceTracker()

def track_vision_analysis(tracker: PerformanceTracker, additional_data: Optional[Dict] = None):
    """Track GPT-4 Vision analysis step"""
    return tracker.track_step("Vision Analysis", additional_data)

def track_product_search(tracker: PerformanceTracker, additional_data: Optional[Dict] = None):
    """Track product search step"""
    return tracker.track_step("Product Search", additional_data)

def track_image_generation(tracker: PerformanceTracker, additional_data: Optional[Dict] = None):
    """Track image generation step"""
    return tracker.track_step("Image Generation", additional_data)

def track_composite_creation(tracker: PerformanceTracker, additional_data: Optional[Dict] = None):
    """Track composite image creation step"""
    return tracker.track_step("Composite Creation", additional_data) 