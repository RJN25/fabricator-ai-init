"""
Configuration file for Fabricator.ai MVP
"""

# Application Settings
APP_NAME = "Fabricator.ai"
APP_VERSION = "1.0.0-MVP"
APP_DESCRIPTION = "AI-Powered CAD Conversion Engine - Proof of Concept"

# Processing Settings
DEFAULT_PRECISION = 7
MAX_PRECISION = 10
MIN_PRECISION = 1

# Shape Detection Settings
SHAPE_CONFIDENCE_THRESHOLD = 70.0
MIN_CONTOUR_AREA = 100
MAX_CONTOUR_AREA = 1000000

# DXF Generation Settings
DXF_VERSION = 'R2010'
DEFAULT_UNITS = 'mm'
LAYER_NAME = 'FABRICATOR_AI'
DEFAULT_COLOR = 1  # Red

# File Upload Settings
ALLOWED_IMAGE_TYPES = ['png', 'jpg', 'jpeg']
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# UI Settings
THEME_COLORS = {
    'primary': '#ff6b35',
    'secondary': '#ff8c42',
    'background': '#0a0a0a',
    'surface': '#1a1a1a',
    'text': '#ffffff',
    'border': '#333333'
}

# Supported Shapes
SUPPORTED_SHAPES = [
    'circle',
    'rectangle', 
    'triangle',
    'hexagon',
    'polygon'
]

# Shape Detection Parameters
SHAPE_DETECTION_PARAMS = {
    'circle': {
        'circularity_threshold': 0.7,
        'min_radius': 5.0,
        'max_radius': 500.0
    },
    'rectangle': {
        'area_ratio_threshold': 0.6,
        'min_aspect_ratio': 0.1,
        'max_aspect_ratio': 10.0
    },
    'triangle': {
        'area_ratio_threshold': 0.3,
        'min_vertices': 3,
        'max_vertices': 3
    },
    'hexagon': {
        'area_ratio_threshold': 0.2,
        'min_vertices': 6,
        'max_vertices': 6
    }
}

# Text Processing Patterns
TEXT_PATTERNS = {
    'dimensions': {
        'radius': r'\b(radius|r)\s*[=:]\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?\b',
        'diameter': r'\b(diameter|d)\s*[=:]\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?\b',
        'width': r'\b(width|w)\s*[=:]\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?\b',
        'height': r'\b(height|h)\s*[=:]\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?\b',
        'length': r'\b(length|l)\s*[=:]\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?\b',
        'side': r'\b(side|s)\s*[=:]\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?\b'
    },
    'units': {
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
}

# Performance Targets (from PoC requirements)
PERFORMANCE_TARGETS = {
    'max_processing_time_seconds': 120,  # <2 minutes
    'target_conversion_accuracy_percent': 90,  # 90%+
    'min_confidence_threshold': 70.0
}

# Future Architecture Placeholders
FUTURE_FEATURES = {
    'vector_database': 'FAISS-based template retrieval system',
    'ai_orchestration': 'LLM execution with guard-rails',
    'quality_control': '3-pass validation system',
    'template_library': 'Write-back system for approved designs',
    'manufacturability': 'Automated validation against foam fabrication standards'
}
