import re
import math
from typing import Dict, Any, Tuple, Optional

class TextProcessor:
    """Processes natural language text descriptions to extract geometric shape information"""
    
    def __init__(self):
        # Common shape keywords and their variations
        self.shape_patterns = {
            'circle': r'\b(circle|round|circular|disk|ring)\b',
            'rectangle': r'\b(rectangle|rect|square|box|rectangular)\b',
            'triangle': r'\b(triangle|triangular|pyramid)\b',
            'hexagon': r'\b(hexagon|hex|hexagonal)\b',
            'polygon': r'\b(polygon|poly|shape|figure)\b'
        }
        
        # Measurement units and their conversions
        self.units = {
            'mm': 1.0,
            'millimeter': 1.0,
            'millimeters': 1.0,
            'cm': 10.0,
            'centimeter': 10.0,
            'centimeters': 10.0,
            'm': 1000.0,
            'meter': 1000.0,
            'meters': 1000.0,
            'in': 25.4,
            'inch': 25.4,
            'inches': 25.4,
            'ft': 304.8,
            'foot': 304.8,
            'feet': 304.8
        }
        
        # Dimension patterns
        self.dimension_patterns = {
            'radius': r'\b(radius|r)\s*[=:]\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?\b',
            'diameter': r'\b(diameter|d)\s*[=:]\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?\b',
            'width': r'\b(width|w)\s*[=:]\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?\b',
            'height': r'\b(height|h)\s*[=:]\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?\b',
            'length': r'\b(length|l)\s*[=:]\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?\b',
            'side': r'\b(side|s)\s*[=:]\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?\b'
        }
    
    def process_text(self, text_input: str, expected_shape: str = "Auto-detect") -> Dict[str, Any]:
        """
        Process text input and extract geometric shape information
        
        Args:
            text_input: Natural language description of the shape
            expected_shape: Expected shape type for validation
        
        Returns:
            Dictionary containing extracted shape information
        """
        try:
            # Normalize text
            normalized_text = self._normalize_text(text_input)
            
            # Detect shape type
            detected_shape = self._detect_shape_type(normalized_text, expected_shape)
            
            # Extract dimensions
            dimensions = self._extract_dimensions(normalized_text)
            
            # Validate and construct shape data
            shape_data = self._construct_shape_data(detected_shape, dimensions, normalized_text)
            
            # Add confidence and metadata
            shape_data = self._add_metadata(shape_data, normalized_text)
            
            return shape_data
            
        except Exception as e:
            raise Exception(f"Text processing failed: {str(e)}")
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for processing"""
        # Convert to lowercase
        normalized = text.lower()
        
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Standardize common abbreviations
        normalized = re.sub(r'\b(r|radius)\b', 'radius', normalized)
        normalized = re.sub(r'\b(d|diameter)\b', 'diameter', normalized)
        normalized = re.sub(r'\b(w|width)\b', 'width', normalized)
        normalized = re.sub(r'\b(h|height)\b', 'height', normalized)
        normalized = re.sub(r'\b(l|length)\b', 'length', normalized)
        normalized = re.sub(r'\b(s|side)\b', 'side', normalized)
        
        return normalized.strip()
    
    def _detect_shape_type(self, text: str, expected_shape: str) -> str:
        """Detect the type of shape from text"""
        # If expected shape is specified and not auto-detect, use it
        if expected_shape != "Auto-detect":
            return expected_shape.lower()
        
        # Try to detect shape from text patterns
        for shape_name, pattern in self.shape_patterns.items():
            if re.search(pattern, text):
                return shape_name
        
        # Default to circle if no shape detected
        return 'circle'
    
    def _extract_dimensions(self, text: str) -> Dict[str, float]:
        """Extract dimensions from text"""
        dimensions = {}
        
        for dim_name, pattern in self.dimension_patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                value = float(match[0])
                unit = match[1] if len(match) > 1 else 'mm'
                
                # Convert to millimeters
                converted_value = self._convert_to_mm(value, unit)
                dimensions[dim_name] = converted_value
        
        # Handle special cases for common shapes
        dimensions = self._handle_special_cases(text, dimensions)
        
        return dimensions
    
    def _handle_special_cases(self, text: str, dimensions: Dict[str, float]) -> Dict[str, float]:
        """Handle special cases for common shape descriptions"""
        # Handle "X by Y" patterns (e.g., "100 by 50")
        size_pattern = r'(\d+(?:\.\d+)?)\s*(?:by|x|×)\s*(\d+(?:\.\d+)?)'
        size_matches = re.findall(size_pattern, text)
        
        if size_matches:
            for match in size_matches:
                val1, val2 = float(match[0]), float(match[1])
                
                # Determine if these are width/height or other dimensions
                if 'circle' in text or 'round' in text:
                    # For circles, this might be diameter
                    if 'diameter' not in dimensions:
                        dimensions['diameter'] = max(val1, val2)
                else:
                    # For other shapes, assume width x height
                    if 'width' not in dimensions:
                        dimensions['width'] = val1
                    if 'height' not in dimensions:
                        dimensions['height'] = val2
        
        # Handle "X mm" patterns without explicit labels
        simple_pattern = r'(\d+(?:\.\d+)?)\s*(mm|cm|m|in|ft)'
        simple_matches = re.findall(simple_pattern, text)
        
        if simple_matches and not dimensions:
            # If no explicit dimensions found, use the first measurement
            value, unit = float(simple_matches[0][0]), simple_matches[0][1]
            converted_value = self._convert_to_mm(value, unit)
            
            if 'circle' in text or 'round' in text:
                dimensions['radius'] = converted_value / 2
            else:
                dimensions['width'] = converted_value
                dimensions['height'] = converted_value
        
        return dimensions
    
    def _convert_to_mm(self, value: float, unit: str) -> float:
        """Convert value to millimeters"""
        unit_lower = unit.lower()
        if unit_lower in self.units:
            return value * self.units[unit_lower]
        else:
            # Default to millimeters
            return value
    
    def _construct_shape_data(self, shape_type: str, dimensions: Dict[str, float], text: str) -> Dict[str, Any]:
        """Construct shape data from detected type and dimensions"""
        shape_data = {
            'type': shape_type,
            'confidence': 85.0,  # Base confidence
            'vertices': self._get_vertex_count(shape_type),
            'area': 0.0,
            'perimeter': 0.0
        }
        
        # Add shape-specific properties
        if shape_type == 'circle':
            shape_data.update(self._construct_circle_data(dimensions))
        elif shape_type == 'rectangle':
            shape_data.update(self._construct_rectangle_data(dimensions))
        elif shape_type == 'triangle':
            shape_data.update(self._construct_triangle_data(dimensions))
        elif shape_type == 'hexagon':
            shape_data.update(self._construct_hexagon_data(dimensions))
        else:
            shape_data.update(self._construct_polygon_data(dimensions))
        
        return shape_data
    
    def _get_vertex_count(self, shape_type: str) -> int:
        """Get the number of vertices for a shape type"""
        vertex_counts = {
            'circle': 0,  # Circles don't have vertices in DXF
            'rectangle': 4,
            'triangle': 3,
            'hexagon': 6,
            'polygon': 8  # Default for custom polygons
        }
        return vertex_counts.get(shape_type, 4)
    
    def _construct_circle_data(self, dimensions: Dict[str, float]) -> Dict[str, Any]:
        """Construct circle data"""
        radius = dimensions.get('radius', 25.0)
        diameter = dimensions.get('diameter', radius * 2)
        
        if 'diameter' in dimensions:
            radius = diameter / 2
        elif 'radius' in dimensions:
            diameter = radius * 2
        
        return {
            'center': (0.0, 0.0),
            'radius': radius,
            'diameter': diameter,
            'area': math.pi * radius * radius,
            'perimeter': math.pi * diameter
        }
    
    def _construct_rectangle_data(self, dimensions: Dict[str, float]) -> Dict[str, Any]:
        """Construct rectangle data"""
        width = dimensions.get('width', 100.0)
        height = dimensions.get('height', 75.0)
        
        # If only one dimension specified, make it square
        if 'width' in dimensions and 'height' not in dimensions:
            height = width
        elif 'height' in dimensions and 'width' not in dimensions:
            width = height
        
        return {
            'center': (0.0, 0.0),
            'width': width,
            'height': height,
            'area': width * height,
            'perimeter': 2 * (width + height)
        }
    
    def _construct_triangle_data(self, dimensions: Dict[str, float]) -> Dict[str, Any]:
        """Construct triangle data"""
        base = dimensions.get('width', dimensions.get('length', 100.0))
        height = dimensions.get('height', 75.0)
        
        # Calculate area and perimeter for equilateral triangle
        area = 0.5 * base * height
        side_length = math.sqrt(base * base + height * height)
        perimeter = 3 * side_length
        
        return {
            'center': (0.0, 0.0),
            'width': base,
            'height': height,
            'area': area,
            'perimeter': perimeter
        }
    
    def _construct_hexagon_data(self, dimensions: Dict[str, float]) -> Dict[str, Any]:
        """Construct hexagon data"""
        side_length = dimensions.get('side', 50.0)
        
        # Regular hexagon calculations
        area = (3 * math.sqrt(3) * side_length * side_length) / 2
        perimeter = 6 * side_length
        
        return {
            'center': (0.0, 0.0),
            'side_length': side_length,
            'width': 2 * side_length,
            'height': math.sqrt(3) * side_length,
            'area': area,
            'perimeter': perimeter
        }
    
    def _construct_polygon_data(self, dimensions: Dict[str, float]) -> Dict[str, Any]:
        """Construct polygon data"""
        side_length = dimensions.get('side', 50.0)
        width = dimensions.get('width', 100.0)
        height = dimensions.get('height', 100.0)
        
        return {
            'center': (0.0, 0.0),
            'side_length': side_length,
            'width': width,
            'height': height,
            'area': width * height * 0.8,  # Approximate
            'perimeter': 8 * side_length  # Approximate
        }
    
    def _add_metadata(self, shape_data: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Add metadata to shape data"""
        # Adjust confidence based on text quality
        confidence_boost = 0
        
        # Boost confidence if dimensions are well-specified
        if len(shape_data) > 5:  # Has multiple properties
            confidence_boost += 5
        
        # Boost confidence if units are specified
        if any(unit in text for unit in ['mm', 'cm', 'm', 'in', 'ft']):
            confidence_boost += 5
        
        # Boost confidence if shape type is explicitly mentioned
        if any(shape in text for shape in ['circle', 'rectangle', 'triangle', 'hexagon']):
            confidence_boost += 5
        
        shape_data['confidence'] = min(100, shape_data['confidence'] + confidence_boost)
        
        # Add timestamp
        import datetime
        shape_data['timestamp'] = datetime.datetime.now().isoformat()
        
        # Add source
        shape_data['source'] = 'text_input'
        
        return shape_data
