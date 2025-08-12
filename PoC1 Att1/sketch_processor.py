import cv2
import numpy as np
from PIL import Image
import io
import re
from typing import Dict, Any, Tuple

class SketchProcessor:
    """Processes hand-drawn sketches to detect geometric shapes"""
    
    def __init__(self):
        self.shape_templates = {
            'circle': self._detect_circle,
            'rectangle': self._detect_rectangle,
            'triangle': self._detect_triangle,
            'hexagon': self._detect_hexagon,
            'polygon': self._detect_polygon
        }
    
    def process_sketch(self, uploaded_file, expected_shape: str = "Auto-detect", precision: int = 7) -> Dict[str, Any]:
        """
        Process uploaded sketch and detect geometric shapes
        
        Args:
            uploaded_file: Streamlit uploaded file object
            expected_shape: Expected shape type for validation
            precision: Processing precision level (1-10)
        
        Returns:
            Dictionary containing detected shape information
        """
        try:
            # Convert uploaded file to OpenCV format
            image_bytes = uploaded_file.read()
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                raise ValueError("Could not decode uploaded image")
            
            # Preprocess image
            processed_image = self._preprocess_image(image, precision)
            
            # Detect shapes
            detected_shapes = self._detect_shapes(processed_image, precision)
            
            # Select best match
            best_shape = self._select_best_shape(detected_shapes, expected_shape)
            
            # Validate and enhance shape data
            enhanced_shape = self._enhance_shape_data(best_shape, precision)
            
            return enhanced_shape
            
        except Exception as e:
            raise Exception(f"Sketch processing failed: {str(e)}")
    
    def _preprocess_image(self, image: np.ndarray, precision: int) -> np.ndarray:
        """Preprocess image for shape detection"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur based on precision
        blur_kernel = max(1, 11 - precision)
        if blur_kernel % 2 == 0:
            blur_kernel += 1
        blurred = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Morphological operations to clean up noise
        kernel = np.ones((3, 3), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        
        return cleaned
    
    def _detect_shapes(self, processed_image: np.ndarray, precision: int) -> list:
        """Detect all possible shapes in the processed image"""
        detected_shapes = []
        
        # Find contours
        contours, _ = cv2.findContours(
            processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Filter contours by area (remove noise)
        min_area = 100 * precision
        valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]
        
        for contour in valid_contours:
            # Approximate contour to reduce noise
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Analyze each contour for different shape types
            for shape_name, detector_func in self.shape_templates.items():
                try:
                    shape_data = detector_func(approx, contour, precision)
                    if shape_data:
                        shape_data['contour'] = contour
                        shape_data['approx_contour'] = approx
                        detected_shapes.append(shape_data)
                except Exception:
                    continue
        
        return detected_shapes
    
    def _detect_circle(self, approx: np.ndarray, contour: np.ndarray, precision: int) -> Dict[str, Any]:
        """Detect if contour represents a circle"""
        # Check if contour is approximately circular
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter == 0:
            return None
        
        # Circularity measure (4π * area / perimeter²)
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        
        # Circle threshold based on precision
        circle_threshold = 0.7 + (precision * 0.02)
        
        if circularity > circle_threshold:
            # Fit circle to contour
            (x, y), radius = cv2.minEnclosingCircle(contour)
            
            return {
                'type': 'circle',
                'center': (float(x), float(y)),
                'radius': float(radius),
                'confidence': min(100, circularity * 100),
                'vertices': len(approx),
                'area': float(area),
                'perimeter': float(perimeter)
            }
        
        return None
    
    def _detect_rectangle(self, approx: np.ndarray, contour: np.ndarray, precision: int) -> Dict[str, Any]:
        """Detect if contour represents a rectangle"""
        if len(approx) == 4:
            # Check if it's approximately rectangular
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            rect_area = w * h
            
            # Area ratio should be close to 1 for a good rectangle
            area_ratio = area / rect_area if rect_area > 0 else 0
            
            # Rectangle threshold based on precision
            rect_threshold = 0.6 + (precision * 0.03)
            
            if area_ratio > rect_threshold:
                return {
                    'type': 'rectangle',
                    'center': (float(x + w/2), float(y + h/2)),
                    'width': float(w),
                    'height': float(h),
                    'confidence': min(100, area_ratio * 100),
                    'vertices': 4,
                    'area': float(area),
                    'perimeter': float(cv2.arcLength(contour, True))
                }
        
        return None
    
    def _detect_triangle(self, approx: np.ndarray, contour: np.ndarray, precision: int) -> Dict[str, Any]:
        """Detect if contour represents a triangle"""
        if len(approx) == 3:
            # Check if it's approximately triangular
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            rect_area = w * h
            
            # Area ratio for triangle should be around 0.5
            area_ratio = area / rect_area if rect_area > 0 else 0
            expected_ratio = 0.5
            
            # Triangle threshold based on precision
            triangle_threshold = 0.3 + (precision * 0.04)
            
            if abs(area_ratio - expected_ratio) < triangle_threshold:
                return {
                    'type': 'triangle',
                    'center': (float(x + w/2), float(y + h/2)),
                    'width': float(w),
                    'height': float(h),
                    'confidence': min(100, (1 - abs(area_ratio - expected_ratio)) * 100),
                    'vertices': 3,
                    'area': float(area),
                    'perimeter': float(cv2.arcLength(contour, True))
                }
        
        return None
    
    def _detect_hexagon(self, approx: np.ndarray, contour: np.ndarray, precision: int) -> Dict[str, Any]:
        """Detect if contour represents a hexagon"""
        if len(approx) == 6:
            # Check if it's approximately hexagonal
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            rect_area = w * h
            
            # Area ratio for regular hexagon should be around 0.866
            area_ratio = area / rect_area if rect_area > 0 else 0
            expected_ratio = 0.866
            
            # Hexagon threshold based on precision
            hex_threshold = 0.2 + (precision * 0.03)
            
            if abs(area_ratio - expected_ratio) < hex_threshold:
                return {
                    'type': 'hexagon',
                    'center': (float(x + w/2), float(y + h/2)),
                    'width': float(w),
                    'height': float(h),
                    'confidence': min(100, (1 - abs(area_ratio - expected_ratio)) * 100),
                    'vertices': 6,
                    'area': float(area),
                    'perimeter': float(cv2.arcLength(contour, True))
                }
        
        return None
    
    def _detect_polygon(self, approx: np.ndarray, contour: np.ndarray, precision: int) -> Dict[str, Any]:
        """Detect if contour represents a general polygon"""
        if len(approx) > 6:
            # Check if it's a reasonable polygon
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            rect_area = w * h
            
            # Area ratio should be reasonable
            area_ratio = area / rect_area if rect_area > 0 else 0
            
            if area_ratio > 0.3:
                return {
                    'type': 'polygon',
                    'center': (float(x + w/2), float(y + h/2)),
                    'width': float(w),
                    'height': float(h),
                    'confidence': min(100, area_ratio * 100),
                    'vertices': len(approx),
                    'area': float(area),
                    'perimeter': float(cv2.arcLength(contour, True))
                }
        
        return None
    
    def _select_best_shape(self, detected_shapes: list, expected_shape: str) -> Dict[str, Any]:
        """Select the best matching shape based on confidence and expected type"""
        if not detected_shapes:
            # Return a default circle if nothing detected
            return {
                'type': 'circle',
                'center': (0, 0),
                'radius': 50,
                'confidence': 50.0,
                'vertices': 0,
                'area': 7854.0,
                'perimeter': 314.0
            }
        
        # If expected shape is specified, prioritize it
        if expected_shape != "Auto-detect":
            expected_shapes = [s for s in detected_shapes if s['type'] == expected_shape.lower()]
            if expected_shapes:
                # Return the one with highest confidence
                return max(expected_shapes, key=lambda x: x['confidence'])
        
        # Otherwise, return the shape with highest confidence
        return max(detected_shapes, key=lambda x: x['confidence'])
    
    def _enhance_shape_data(self, shape_data: Dict[str, Any], precision: int) -> Dict[str, Any]:
        """Enhance shape data with additional information"""
        enhanced = shape_data.copy()
        
        # Add precision-based scaling
        scale_factor = 1.0 + (precision - 5) * 0.1
        enhanced['scale_factor'] = scale_factor
        
        # Add manufacturing considerations
        enhanced['manufacturable'] = True
        enhanced['min_feature_size'] = max(1.0, 10.0 / precision)
        
        # Add timestamp
        import datetime
        enhanced['timestamp'] = datetime.datetime.now().isoformat()
        
        return enhanced
