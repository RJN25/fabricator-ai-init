#!/usr/bin/env python3
"""
Sample data generator for Fabricator.ai MVP testing
Creates simple test images and data for validation
"""

import numpy as np
from PIL import Image, ImageDraw
import os
from pathlib import Path

def create_sample_circle():
    """Create a sample circle image"""
    # Create a white image with black background
    img = Image.new('RGB', (400, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a circle
    center = (200, 200)
    radius = 80
    bbox = (center[0] - radius, center[1] - radius, 
            center[0] + radius, center[1] + radius)
    
    draw.ellipse(bbox, outline='black', width=3)
    
    # Add some text
    draw.text((10, 10), "Sample Circle", fill='black')
    draw.text((10, 30), f"Radius: {radius}px", fill='black')
    
    return img

def create_sample_rectangle():
    """Create a sample rectangle image"""
    # Create a white image with black background
    img = Image.new('RGB', (400, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a rectangle
    rect = (50, 50, 350, 250)
    draw.rectangle(rect, outline='black', width=3)
    
    # Add some text
    draw.text((10, 10), "Sample Rectangle", fill='black')
    draw.text((10, 30), "300x200 pixels", fill='black')
    
    return img

def create_sample_triangle():
    """Create a sample triangle image"""
    # Create a white image with black background
    img = Image.new('RGB', (400, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a triangle
    points = [(200, 50), (100, 250), (300, 250)]
    draw.polygon(points, outline='black', width=3)
    
    # Add some text
    draw.text((10, 10), "Sample Triangle", fill='black')
    draw.text((10, 30), "Equilateral", fill='black')
    
    return img

def create_sample_hexagon():
    """Create a sample hexagon image"""
    # Create a white image with black background
    img = Image.new('RGB', (400, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    # Calculate hexagon points
    center = (200, 200)
    radius = 80
    points = []
    
    for i in range(6):
        angle = i * 60 * np.pi / 180
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        points.append((x, y))
    
    # Draw hexagon
    draw.polygon(points, outline='black', width=3)
    
    # Add some text
    draw.text((10, 10), "Sample Hexagon", fill='black')
    draw.text((10, 30), f"Side: {radius}px", fill='black')
    
    return img

def create_sample_data_directory():
    """Create sample data directory with test images"""
    # Create data directory
    data_dir = Path("sample_data")
    data_dir.mkdir(exist_ok=True)
    
    # Create sample images
    samples = [
        ("sample_circle.png", create_sample_circle()),
        ("sample_rectangle.png", create_sample_rectangle()),
        ("sample_triangle.png", create_sample_triangle()),
        ("sample_hexagon.png", create_sample_hexagon())
    ]
    
    print("🔧 Creating sample data for Fabricator.ai MVP...")
    
    for filename, img in samples:
        filepath = data_dir / filename
        img.save(filepath)
        print(f"  ✅ Created: {filepath}")
    
    # Create a README for the sample data
    readme_content = """# Sample Data for Fabricator.ai MVP

This directory contains sample images for testing the MVP functionality.

## Available Samples

- **sample_circle.png**: Simple circle with 80px radius
- **sample_rectangle.png**: Rectangle 300x200 pixels
- **sample_triangle.png**: Equilateral triangle
- **sample_hexagon.png**: Regular hexagon with 80px side length

## How to Use

1. Upload these images in the Streamlit interface
2. Test shape detection accuracy
3. Verify DXF generation
4. Compare confidence scores

## Expected Results

- **Circle**: Should detect as circle with ~90%+ confidence
- **Rectangle**: Should detect as rectangle with ~85%+ confidence  
- **Triangle**: Should detect as triangle with ~80%+ confidence
- **Hexagon**: Should detect as hexagon with ~75%+ confidence

## Notes

- These are clean, simple shapes for testing
- Real-world sketches may have lower confidence scores
- Adjust precision levels for optimal results
"""
    
    readme_path = data_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"  ✅ Created: {readme_path}")
    print()
    print("🎯 Sample data ready for testing!")
    print("💡 Upload these images in the Streamlit UI to test shape detection.")
    print()

def main():
    """Main function to create sample data"""
    try:
        create_sample_data_directory()
        print("✅ Sample data generation completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Sample data generation failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
