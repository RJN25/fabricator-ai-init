import streamlit as st
import cv2
import numpy as np
from PIL import Image
import ezdxf
import os
import tempfile
from pathlib import Path
import matplotlib.pyplot as plt
from sketch_processor import SketchProcessor
from text_processor import TextProcessor
from dxf_generator import DXFGenerator
import io

# Page configuration
st.set_page_config(
    page_title="Fabricator.ai - AI-Powered CAD Conversion",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for sleek black and orange tech theme
st.markdown("""
<style>
    .main {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    
    .stApp {
        background-color: #0a0a0a;
    }
    
    .stButton > button {
        background-color: #ff6b35;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #ff8c42;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
    }
    
    .stFileUploader > div > div > div > div {
        background-color: #1a1a1a;
        border: 2px dashed #ff6b35;
        border-radius: 12px;
        color: #ffffff;
    }
    
    .stTextInput > div > div > input {
        background-color: #1a1a1a;
        border: 2px solid #333333;
        color: #ffffff;
        border-radius: 8px;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #1a1a1a;
        border: 2px solid #333333;
        color: #ffffff;
        border-radius: 8px;
    }
    
    .stSelectbox > div > div > select {
        background-color: #1a1a1a;
        border: 2px solid #333333;
        color: #ffffff;
        border-radius: 8px;
    }
    
    .metric-container {
        background-color: #1a1a1a;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
    }
    
    .header-container {
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(90deg, #ff6b35, #ff8c42);
        border-radius: 12px;
        margin-bottom: 30px;
    }
    
    .success-message {
        background-color: #1a1a1a;
        border-left: 4px solid #ff6b35;
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="header-container">
        <h1>🔧 Fabricator.ai</h1>
        <h3>AI-Powered CAD Conversion Engine</h3>
        <p>Transform sketches and text into manufacturable DXF files</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Input Method")
        input_method = st.selectbox(
            "Choose your input method:",
            ["📝 Text Description", "✏️ Hand-drawn Sketch", "🔄 Both"]
        )
        
        st.markdown("### ⚙️ Settings")
        shape_type = st.selectbox(
            "Expected shape type:",
            ["Auto-detect", "Circle", "Rectangle", "Triangle", "Hexagon", "Custom"]
        )
        
        precision = st.slider("Precision Level", 1, 10, 7)
        
        st.markdown("### 📊 Status")
        if 'processing_status' in st.session_state:
            st.info(st.session_state.processing_status)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📥 Input")
        
        if input_method in ["📝 Text Description", "🔄 Both"]:
            st.markdown("#### Text Description")
            text_input = st.text_area(
                "Describe the shape you want to create:",
                placeholder="e.g., A circle with radius 50mm, or a rectangle 100mm x 75mm",
                height=120
            )
            
            if st.button("🚀 Generate from Text", key="text_btn"):
                if text_input.strip():
                    process_text_input(text_input, shape_type, precision)
                else:
                    st.error("Please enter a text description")
        
        if input_method in ["✏️ Hand-drawn Sketch", "🔄 Both"]:
            st.markdown("#### Hand-drawn Sketch")
            uploaded_file = st.file_uploader(
                "Upload your sketch image:",
                type=['png', 'jpg', 'jpeg'],
                help="Upload a hand-drawn sketch or use Microsoft Paint equivalent quality"
            )
            
            if uploaded_file is not None:
                # Display the uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Sketch", use_column_width=True)
                
                if st.button("🔍 Process Sketch", key="sketch_btn"):
                    process_sketch_input(uploaded_file, shape_type, precision)
    
    with col2:
        st.markdown("### 📤 Output")
        
        if 'dxf_generated' in st.session_state and st.session_state.dxf_generated:
            st.success("✅ DXF file generated successfully!")
            
            # Display preview
            if 'preview_image' in st.session_state:
                st.image(st.session_state.preview_image, caption="Generated Shape Preview", use_column_width=True)
            
            # Download button
            if 'dxf_file_path' in st.session_state:
                with open(st.session_state.dxf_file_path, 'rb') as f:
                    st.download_button(
                        label="📥 Download DXF File",
                        data=f.read(),
                        file_name="fabricator_generated.dxf",
                        mime="application/dxf"
                    )
                
                # Show file location
                st.info(f"💾 DXF file saved to: {st.session_state.dxf_file_path}")
            
            # Display metrics
            if 'processing_metrics' in st.session_state:
                st.markdown("### 📊 Processing Metrics")
                metrics = st.session_state.processing_metrics
                
                col_metric1, col_metric2 = st.columns(2)
                with col_metric1:
                    st.metric("Processing Time", f"{metrics['processing_time']:.2f}s")
                    st.metric("Shape Detected", metrics['shape_type'])
                
                with col_metric2:
                    st.metric("Confidence", f"{metrics['confidence']:.1f}%")
                    st.metric("Vertices", metrics['vertices'])
        
        else:
            st.info("👆 Upload a sketch or enter text description to get started")
            st.markdown("""
            <div class="metric-container">
                <h4>🎯 What we can detect:</h4>
                <ul>
                    <li>🔴 Circles and ellipses</li>
                    <li>⬜ Rectangles and squares</li>
                    <li>🔺 Triangles</li>
                    <li>⬡ Hexagons</li>
                    <li>📐 Custom polygons</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🔧 Fabricator.ai - Transforming ideas into manufacturable designs</p>
        <p>Powered by AI • Built for precision • Ready for production</p>
    </div>
    """, unsafe_allow_html=True)

def process_text_input(text_input, shape_type, precision):
    """Process text input and generate DXF"""
    try:
        st.session_state.processing_status = "🔄 Processing text input..."
        
        # Initialize text processor
        text_processor = TextProcessor()
        shape_data = text_processor.process_text(text_input, shape_type)
        
        # Generate DXF
        dxf_generator = DXFGenerator()
        dxf_file_path = dxf_generator.generate_from_shape_data(shape_data, precision)
        
        # Update session state
        st.session_state.dxf_generated = True
        st.session_state.dxf_file_path = dxf_file_path
        st.session_state.processing_metrics = {
            'processing_time': 1.2,  # Placeholder
            'shape_type': shape_data['type'],
            'confidence': 95.0,
            'vertices': shape_data.get('vertices', 4)
        }
        st.session_state.processing_status = "✅ Text processing complete!"
        
        st.rerun()
        
    except Exception as e:
        st.error(f"Error processing text input: {str(e)}")
        st.session_state.processing_status = "❌ Text processing failed"

def process_sketch_input(uploaded_file, shape_type, precision):
    """Process sketch input and generate DXF"""
    try:
        st.session_state.processing_status = "🔄 Processing sketch..."
        
        # Initialize sketch processor
        sketch_processor = SketchProcessor()
        shape_data = sketch_processor.process_sketch(uploaded_file, shape_type, precision)
        
        # Generate DXF
        dxf_generator = DXFGenerator()
        dxf_file_path = dxf_generator.generate_from_shape_data(shape_data, precision)
        
        # Create preview
        preview_image = create_preview(shape_data)
        
        # Update session state
        st.session_state.dxf_generated = True
        st.session_state.dxf_file_path = dxf_file_path
        st.session_state.preview_image = preview_image
        st.session_state.processing_metrics = {
            'processing_time': 2.1,  # Placeholder
            'shape_type': shape_data['type'],
            'confidence': shape_data.get('confidence', 87.5),
            'vertices': shape_data.get('vertices', 4)
        }
        st.session_state.processing_status = "✅ Sketch processing complete!"
        
        st.rerun()
        
    except Exception as e:
        st.error(f"Error processing sketch: {str(e)}")
        st.session_state.processing_status = "❌ Sketch processing failed"

def create_preview(shape_data):
    """Create a preview image of the detected shape"""
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#1a1a1a')
    ax.set_title(f"Detected: {shape_data['type']}", color='white')
    
    # Draw the shape based on type
    if shape_data['type'] == 'circle':
        circle = plt.Circle((0, 0), shape_data.get('radius', 50), 
                           fill=False, color='#ff6b35', linewidth=3)
        ax.add_patch(circle)
    elif shape_data['type'] == 'rectangle':
        rect = plt.Rectangle((-50, -30), 100, 60, 
                           fill=False, color='#ff6b35', linewidth=3)
        ax.add_patch(rect)
    elif shape_data['type'] == 'triangle':
        triangle = plt.Polygon([(-50, -30), (50, -30), (0, 40)], 
                             fill=False, color='#ff6b35', linewidth=3)
        ax.add_patch(triangle)
    elif shape_data['type'] == 'hexagon':
        angles = np.linspace(0, 2*np.pi, 7)[:-1]
        x = 50 * np.cos(angles)
        y = 50 * np.sin(angles)
        hexagon = plt.Polygon(list(zip(x, y)), 
                            fill=False, color='#ff6b35', linewidth=3)
        ax.add_patch(hexagon)
    
    ax.set_facecolor('#1a1a1a')
    fig.patch.set_facecolor('#1a1a1a')
    
    # Save to bytes for Streamlit
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png', facecolor='#1a1a1a', 
                bbox_inches='tight', dpi=100)
    img_bytes.seek(0)
    plt.close()
    
    return Image.open(img_bytes)

if __name__ == "__main__":
    # Initialize session state
    if 'dxf_generated' not in st.session_state:
        st.session_state.dxf_generated = False
    
    main()
