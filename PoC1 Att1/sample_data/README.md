# Sample Data for Fabricator.ai MVP

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
