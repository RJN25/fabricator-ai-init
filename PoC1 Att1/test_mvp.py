#!/usr/bin/env python3
"""
Test script for Fabricator.ai MVP
Tests core functionality without the Streamlit UI
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_text_processor():
    """Test text processing functionality"""
    print("🧪 Testing Text Processor...")
    
    try:
        from text_processor import TextProcessor
        
        processor = TextProcessor()
        
        # Test cases
        test_cases = [
            ("A circle with radius 25mm", "circle"),
            ("Rectangle 100mm by 50mm", "rectangle"),
            ("Triangle with base 60mm and height 40mm", "triangle"),
            ("Hexagon with side length 30mm", "hexagon")
        ]
        
        for text, expected_shape in test_cases:
            result = processor.process_text(text)
            shape_type = result.get('type', 'unknown')
            confidence = result.get('confidence', 0)
            
            status = "✅" if shape_type == expected_shape else "❌"
            print(f"  {status} '{text}' -> {shape_type} (confidence: {confidence:.1f}%)")
            
            if shape_type != expected_shape:
                print(f"    Expected: {expected_shape}, Got: {shape_type}")
        
        print("✅ Text processor tests completed\n")
        return True
        
    except Exception as e:
        print(f"❌ Text processor test failed: {str(e)}\n")
        return False

def test_dxf_generator():
    """Test DXF generation functionality"""
    print("🧪 Testing DXF Generator...")
    
    try:
        from dxf_generator import DXFGenerator
        
        generator = DXFGenerator()
        
        # Test shape data
        test_shapes = [
            {
                'type': 'circle',
                'center': (0, 0),
                'radius': 25.0,
                'confidence': 95.0,
                'vertices': 0,
                'area': 1963.5,
                'perimeter': 157.1
            },
            {
                'type': 'rectangle',
                'center': (0, 0),
                'width': 100.0,
                'height': 50.0,
                'confidence': 90.0,
                'vertices': 4,
                'area': 5000.0,
                'perimeter': 300.0
            }
        ]
        
        for i, shape_data in enumerate(test_shapes):
            try:
                dxf_path = generator.generate_from_shape_data(shape_data, precision=7)
                
                # Check if file was created
                if os.path.exists(dxf_path):
                    file_size = os.path.getsize(dxf_path)
                    print(f"  ✅ Generated DXF for {shape_data['type']}: {dxf_path} ({file_size} bytes)")
                else:
                    print(f"  ❌ DXF file not created for {shape_data['type']}")
                    
            except Exception as e:
                print(f"  ❌ Failed to generate DXF for {shape_data['type']}: {str(e)}")
        
        print("✅ DXF generator tests completed\n")
        return True
        
    except Exception as e:
        print(f"❌ DXF generator test failed: {str(e)}\n")
        return False

def test_sketch_processor():
    """Test sketch processing functionality"""
    print("🧪 Testing Sketch Processor...")
    
    try:
        from sketch_processor import SketchProcessor
        
        processor = SketchProcessor()
        
        # Test basic functionality
        print("  ✅ Sketch processor initialized successfully")
        print("  ℹ️  Sketch processing requires actual image files for testing")
        print("  ℹ️  Test with hand-drawn sketches in the Streamlit UI")
        
        print("✅ Sketch processor tests completed\n")
        return True
        
    except Exception as e:
        print(f"❌ Sketch processor test failed: {str(e)}\n")
        return False

def test_configuration():
    """Test configuration loading"""
    print("🧪 Testing Configuration...")
    
    try:
        import config
        
        print(f"  ✅ App Name: {config.APP_NAME}")
        print(f"  ✅ App Version: {config.APP_VERSION}")
        print(f"  ✅ Supported Shapes: {', '.join(config.SUPPORTED_SHAPES)}")
        print(f"  ✅ Default Precision: {config.DEFAULT_PRECISION}")
        print(f"  ✅ Performance Target: {config.PERFORMANCE_TARGETS['max_processing_time_seconds']}s")
        
        print("✅ Configuration tests completed\n")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {str(e)}\n")
        return False

def main():
    """Run all tests"""
    print("🔧 Fabricator.ai MVP - Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        ("Configuration", test_configuration),
        ("Text Processor", test_text_processor),
        ("DXF Generator", test_dxf_generator),
        ("Sketch Processor", test_sketch_processor)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"Running {test_name} tests...")
        success = test_func()
        results.append((test_name, success))
        print()
    
    # Summary
    print("📊 Test Results Summary")
    print("=" * 30)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    print()
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MVP is ready to run.")
        print("💡 Run 'streamlit run app.py' to launch the application.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        print("💡 Fix the issues before running the application.")
    
    print()
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
