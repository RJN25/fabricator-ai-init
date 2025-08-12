import ezdxf
import math
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, List, Tuple
from datetime import datetime

class DXFGenerator:
    """Generates DXF files from shape data"""
    
    def __init__(self):
        self.dxf_version = 'R2010'  # AutoCAD 2010 format
        self.units = 'mm'  # Default units
        self.layer_name = 'FABRICATOR_AI'
        self.color = 1  # Red color (AutoCAD color index)
        
        # Create generated_dxf subfolder
        self.output_dir = Path("generated_dxf")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_from_shape_data(self, shape_data: Dict[str, Any], precision: int = 7) -> str:
        """
        Generate DXF file from shape data
        
        Args:
            shape_data: Dictionary containing shape information
            precision: Precision level for DXF generation
        
        Returns:
            Path to generated DXF file
        """
        try:
            # Create new DXF document
            doc = ezdxf.new(self.dxf_version)
            
            # Set up modelspace
            msp = doc.modelspace()
            
            # Create layer
            self._create_layer(doc)
            
            # Generate shape based on type
            shape_type = shape_data.get('type', 'circle')
            
            if shape_type == 'circle':
                self._generate_circle(msp, shape_data, precision)
            elif shape_type == 'rectangle':
                self._generate_rectangle(msp, shape_data, precision)
            elif shape_type == 'triangle':
                self._generate_triangle(msp, shape_data, precision)
            elif shape_type == 'hexagon':
                self._generate_hexagon(msp, shape_data, precision)
            else:
                self._generate_polygon(msp, shape_data, precision)
            
            # Add metadata and annotations
            self._add_metadata(msp, shape_data, precision)
            
            # Save DXF file
            dxf_file_path = self._save_dxf(doc, shape_data)
            
            return dxf_file_path
            
        except Exception as e:
            raise Exception(f"DXF generation failed: {str(e)}")
    
    def _create_layer(self, doc: ezdxf.document.Drawing):
        """Create and configure layer for Fabricator.ai"""
        try:
            # Create layer if it doesn't exist
            if self.layer_name not in doc.layers:
                layer = doc.layers.new(self.layer_name)
                layer.color = self.color
                layer.linetype = 'CONTINUOUS'
        except Exception:
            # Layer might already exist, continue
            pass
    
    def _generate_circle(self, msp, shape_data: Dict[str, Any], precision: int):
        """Generate circle in DXF"""
        center = shape_data.get('center', (0.0, 0.0))
        radius = shape_data.get('radius', 25.0)
        
        # Apply precision scaling
        scaled_radius = radius * (1.0 + (precision - 5) * 0.05)
        
        # Create circle
        circle = msp.add_circle(
            center=center,
            radius=scaled_radius,
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color
            }
        )
        
        # Add center point marker
        msp.add_point(
            center,
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color
            }
        )
        
        # Add radius dimension line
        self._add_radius_dimension(msp, center, scaled_radius)
    
    def _generate_rectangle(self, msp, shape_data: Dict[str, Any], precision: int):
        """Generate rectangle in DXF"""
        center = shape_data.get('center', (0.0, 0.0))
        width = shape_data.get('width', 100.0)
        height = shape_data.get('height', 75.0)
        
        # Apply precision scaling
        scaled_width = width * (1.0 + (precision - 5) * 0.05)
        scaled_height = height * (1.0 + (precision - 5) * 0.05)
        
        # Calculate corner points
        half_w = scaled_width / 2
        half_h = scaled_height / 2
        
        corners = [
            (center[0] - half_w, center[1] - half_h),
            (center[0] + half_w, center[1] - half_h),
            (center[0] + half_w, center[1] + half_h),
            (center[0] - half_w, center[1] + half_h),
            (center[0] - half_w, center[1] - half_h)  # Close the rectangle
        ]
        
        # Create polyline
        msp.add_lwpolyline(
            corners,
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'closed': True
            }
        )
        
        # Add center point marker
        msp.add_point(
            center,
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color
            }
        )
        
        # Add dimension lines
        self._add_rectangle_dimensions(msp, center, scaled_width, scaled_height)
    
    def _generate_triangle(self, msp, shape_data: Dict[str, Any], precision: int):
        """Generate triangle in DXF"""
        center = shape_data.get('center', (0.0, 0.0))
        width = shape_data.get('width', 100.0)
        height = shape_data.get('height', 75.0)
        
        # Apply precision scaling
        scaled_width = width * (1.0 + (precision - 5) * 0.05)
        scaled_height = height * (1.0 + (precision - 5) * 0.05)
        
        # Calculate triangle vertices (equilateral)
        half_w = scaled_width / 2
        half_h = scaled_height / 2
        
        vertices = [
            (center[0] - half_w, center[1] - half_h),  # Bottom left
            (center[0] + half_w, center[1] - half_h),  # Bottom right
            (center[0], center[1] + half_h),           # Top center
            (center[0] - half_w, center[1] - half_h)   # Close the triangle
        ]
        
        # Create polyline
        msp.add_lwpolyline(
            vertices,
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'closed': True
            }
        )
        
        # Add center point marker
        msp.add_point(
            center,
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color
            }
        )
        
        # Add dimension lines
        self._add_triangle_dimensions(msp, center, scaled_width, scaled_height)
    
    def _generate_hexagon(self, msp, shape_data: Dict[str, Any], precision: int):
        """Generate hexagon in DXF"""
        center = shape_data.get('center', (0.0, 0.0))
        side_length = shape_data.get('side_length', 50.0)
        
        # Apply precision scaling
        scaled_side = side_length * (1.0 + (precision - 5) * 0.05)
        
        # Calculate hexagon vertices
        vertices = []
        for i in range(6):
            angle = i * math.pi / 3
            x = center[0] + scaled_side * math.cos(angle)
            y = center[1] + scaled_side * math.sin(angle)
            vertices.append((x, y))
        
        # Close the hexagon
        vertices.append(vertices[0])
        
        # Create polyline
        msp.add_lwpolyline(
            vertices,
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'closed': True
            }
        )
        
        # Add center point marker
        msp.add_point(
            center,
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color
            }
        )
        
        # Add dimension lines
        self._add_hexagon_dimensions(msp, center, scaled_side)
    
    def _generate_polygon(self, msp, shape_data: Dict[str, Any], precision: int):
        """Generate custom polygon in DXF"""
        center = shape_data.get('center', (0.0, 0.0))
        side_length = shape_data.get('side_length', 50.0)
        
        # Apply precision scaling
        scaled_side = side_length * (1.0 + (precision - 5) * 0.05)
        
        # Create octagon as default polygon
        vertices = []
        for i in range(8):
            angle = i * math.pi / 4
            x = center[0] + scaled_side * math.cos(angle)
            y = center[1] + scaled_side * math.sin(angle)
            vertices.append((x, y))
        
        # Close the polygon
        vertices.append(vertices[0])
        
        # Create polyline
        msp.add_lwpolyline(
            vertices,
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'closed': True
            }
        )
        
        # Add center point marker
        msp.add_point(
            center,
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color
            }
        )
    
    def _add_radius_dimension(self, msp, center: Tuple[float, float], radius: float):
        """Add radius dimension line for circle"""
        # Create radius line
        end_point = (center[0] + radius, center[1])
        
        msp.add_line(
            start=center,
            end=end_point,
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'linetype': 'DASHDOT'
            }
        )
        
        # Add radius text
        text = msp.add_text(
            f"R{radius:.1f}",
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'height': radius * 0.1
            }
        )
        text.dxf.insert = (center[0] + radius/2, center[1] + radius/2, 0)
    
    def _add_rectangle_dimensions(self, msp, center: Tuple[float, float], width: float, height: float):
        """Add dimension lines for rectangle"""
        half_w = width / 2
        half_h = height / 2
        
        # Width dimension
        msp.add_line(
            start=(center[0] - half_w, center[1] - half_h - 10),
            end=(center[0] + half_w, center[1] - half_h - 10),
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'linetype': 'DASHDOT'
            }
        )
        
        # Height dimension
        msp.add_line(
            start=(center[0] - half_w - 10, center[1] - half_h),
            end=(center[0] - half_w - 10, center[1] + half_h),
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'linetype': 'DASHDOT'
            }
        )
        
        # Add dimension text
        width_text = msp.add_text(
            f"W{width:.1f}",
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'height': min(width, height) * 0.1
            }
        )
        width_text.dxf.insert = (center[0], center[1] - half_h - 15, 0)
        
        height_text = msp.add_text(
            f"H{height:.1f}",
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'height': min(width, height) * 0.1
            }
        )
        height_text.dxf.insert = (center[0] - half_w - 15, center[1], 0)
    
    def _add_triangle_dimensions(self, msp, center: Tuple[float, float], width: float, height: float):
        """Add dimension lines for triangle"""
        half_w = width / 2
        half_h = height / 2
        
        # Base dimension
        msp.add_line(
            start=(center[0] - half_w, center[1] - half_h - 10),
            end=(center[0] + half_w, center[1] - half_h - 10),
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'linetype': 'DASHDOT'
            }
        )
        
        # Height dimension
        msp.add_line(
            start=(center[0] - half_w - 10, center[1] - half_h),
            end=(center[0] - half_w - 10, center[1] + half_h),
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'linetype': 'DASHDOT'
            }
        )
        
        # Add dimension text
        base_text = msp.add_text(
            f"B{width:.1f}",
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'height': min(width, height) * 0.1
            }
        )
        base_text.dxf.insert = (center[0], center[1] - half_h - 15, 0)
        
        height_text = msp.add_text(
            f"H{height:.1f}",
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'height': min(width, height) * 0.1
            }
        )
        height_text.dxf.insert = (center[0] - half_w - 15, center[1], 0)
    
    def _add_hexagon_dimensions(self, msp, center: Tuple[float, float], side_length: float):
        """Add dimension lines for hexagon"""
        # Add side length dimension
        start_point = (center[0] + side_length, center[1])
        end_point = (center[0] + side_length * 1.5, center[1] + side_length * 0.866)
        
        msp.add_line(
            start=start_point,
            end=end_point,
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'linetype': 'DASHDOT'
            }
        )
        
        # Add side length text
        text = msp.add_text(
            f"S{side_length:.1f}",
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'height': side_length * 0.1
            }
        )
        text.dxf.insert = (center[0] + side_length * 1.25, center[1] + side_length * 0.433, 0)
    
    def _add_metadata(self, msp, shape_data: Dict[str, Any], precision: int):
        """Add metadata and annotations to DXF"""
        # Add title block
        title_text = f"FABRICATOR.AI - {shape_data.get('type', 'shape').upper()}"
        title = msp.add_text(
            title_text,
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'height': 5.0
            }
        )
        title.dxf.insert = (0, -200, 0)
        
        # Add timestamp
        timestamp = shape_data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        timestamp_text = msp.add_text(
            f"Generated: {timestamp}",
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'height': 3.0
            }
        )
        timestamp_text.dxf.insert = (0, -210, 0)
        
        # Add confidence score
        confidence = shape_data.get('confidence', 0.0)
        confidence_text = msp.add_text(
            f"Confidence: {confidence:.1f}%",
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'height': 3.0
            }
        )
        confidence_text.dxf.insert = (0, -220, 0)
        
        # Add precision level
        precision_text = msp.add_text(
            f"Precision: {precision}/10",
            dxfattribs={
                'layer': self.layer_name,
                'color': self.color,
                'height': 3.0
            }
        )
        precision_text.dxf.insert = (0, -230, 0)
    
    def _save_dxf(self, doc: ezdxf.document.Drawing, shape_data: Dict[str, Any]) -> str:
        """Save DXF file and return path"""
        try:
            # Generate filename with timestamp
            shape_type = shape_data.get('type', 'shape')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"fabricator_ai_{shape_type}_{timestamp}.dxf"
            
            # Create full path in generated_dxf subfolder
            file_path = self.output_dir / filename
            
            # Save DXF
            doc.saveas(str(file_path))
            
            return str(file_path)
            
        except Exception as e:
            raise Exception(f"Failed to save DXF file: {str(e)}")
    
    def cleanup_temp_file(self, file_path: str):
        """Clean up temporary DXF file (kept for backward compatibility)"""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception:
            pass  # Ignore cleanup errors
