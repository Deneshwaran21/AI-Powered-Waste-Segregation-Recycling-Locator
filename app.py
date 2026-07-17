import streamlit as st
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import os

st.set_page_config(
    page_title="AI Waste Sorter",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0a0f1a 0%, #1a2332 50%, #0f1a2e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hero Section */
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00f5a0 0%, #00d9f5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 1rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #94a3b8;
        text-align: center;
        max-width: 700px;
        margin: 0 auto 2rem auto;
        font-weight: 300;
        line-height: 1.6;
    }
    
    .stats-badge {
        display: inline-block;
        background: rgba(0, 245, 160, 0.15);
        border: 1px solid rgba(0, 245, 160, 0.3);
        border-radius: 50px;
        padding: 0.4rem 1.2rem;
        color: #00f5a0;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0 auto;
        text-align: center;
    }
    
    /* Upload Area */
    .upload-container {
        background: rgba(255, 255, 255, 0.03);
        border: 2px dashed rgba(255, 255, 255, 0.15);
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .upload-container:hover {
        border-color: #00f5a0;
        background: rgba(0, 245, 160, 0.05);
    }
    
    .upload-icon {
        font-size: 4rem;
        margin-bottom: 0.5rem;
    }
    
    .upload-text {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 300;
    }
    
    .upload-hint {
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    
    /* Result Cards */
    .result-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-top: 2rem;
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .result-emoji {
        font-size: 5rem;
        text-align: center;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .result-label {
        color: #e2e8f0;
        font-size: 1.5rem;
        font-weight: 600;
        text-align: center;
    }
    
    .result-confidence {
        color: #00f5a0;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
    }
    
    .result-confidence-label {
        color: #64748b;
        font-size: 0.85rem;
        text-align: center;
        font-weight: 300;
    }
    
    /* Recycler Cards */
    .recycler-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        border-left: 4px solid #00f5a0;
        margin-bottom: 0.8rem;
        transition: all 0.2s ease;
    }
    
    .recycler-card:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateX(5px);
    }
    
    .recycler-name {
        color: #e2e8f0;
        font-weight: 600;
        font-size: 1.05rem;
    }
    
    .recycler-address {
        color: #94a3b8;
        font-size: 0.9rem;
        font-weight: 300;
    }
    
    .recycler-distance {
        color: #00f5a0;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* Progress Bar Custom */
    .stProgress > div > div {
        background: linear-gradient(90deg, #00f5a0, #00d9f5) !important;
        border-radius: 50px !important;
    }
    
    /* Button Custom */
    .stButton > button {
        background: linear-gradient(135deg, #00f5a0, #00d9f5) !important;
        color: #0a0f1a !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.7rem 2.5rem !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 30px rgba(0, 245, 160, 0.3);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #475569;
        font-size: 0.85rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# HERO SECTION

st.markdown('<div class="hero-title">♻️ AI Waste Sorter</div>', unsafe_allow_html=True)
st.markdown("""
<div class="hero-subtitle">
    Snap a photo of your waste, and our AI will identify the material 
    and connect you with nearby recycling agents.
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center;">
        <span class="stats-badge">🧠 95.96% Accuracy • 5 Categories • Powered by ResNet-50</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# LOAD THE AI MODEL

@st.cache_resource
def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Rebuild the exact same architecture used in training
    model = models.resnet50(weights=None)
    num_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Linear(num_features, 512),
        nn.ReLU(),
        nn.Dropout(0.5),
        nn.Linear(512, 5)
    )
    
    # Load the trained weights
    model.load_state_dict(torch.load("waste_model.pth", map_location=device))
    model = model.to(device)
    model.eval()
    return model, device

# Load the model (cached so it only runs once)
model, device = load_model()


# CLASSES & RECYCLERS 

CLASS_NAMES = ["cardboard_paper", "chips_packets", "metal_cans", "organic_kitchen", "plastic_bottles"]

CLASS_EMOJIS = {
    "cardboard_paper": "📦",
    "chips_packets": "🍟",
    "metal_cans": "🥫",
    "organic_kitchen": "🍃",
    "plastic_bottles": "🧴"
}

RECYCLERS = {
    "cardboard_paper": [{"name": "PaperCycle Hub", "address": "12/B, Nehru Nagar", "distance": "3.1 km"}],
    "chips_packets": [{"name": "GreenLayer Solutions", "address": "Shop 5, MG Road", "distance": "1.8 km"}],
    "metal_cans": [{"name": "MetalMithra", "address": "G-7, Auto Nagar", "distance": "4.0 km"}],
    "organic_kitchen": [{"name": "Compost Kings", "address": "Farm 23, Outer Ring Road", "distance": "5.2 km"}],
    "plastic_bottles": [{"name": "EcoPlast Recyclers", "address": "Plot 42, Industrial Area", "distance": "2.3 km"}]
}

# Image preprocessing (must match training)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# MAIN LAYOUT: Upload + Results

left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown("""
    <div class="upload-container">
        <div class="upload-icon">📸</div>
        <div class="upload-text">Drop your waste photo here</div>
        <div class="upload-hint">Supports JPG, JPEG, PNG</div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

with right_col:
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="📸 Your Waste", use_container_width=True)
    else:
        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.03);
            border-radius: 20px;
            padding: 4rem 2rem;
            text-align: center;
            border: 1px dashed rgba(255,255,255,0.08);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        ">
            <div style="font-size: 4rem; opacity: 0.3;">🔄</div>
            <div style="color: #475569; margin-top: 1rem; font-weight: 300;">Upload an image to begin</div>
        </div>
        """, unsafe_allow_html=True)


# PREDICT BUTTON

if uploaded_file is not None:
    if st.button("🔍 Identify & Find Recyclers", type="primary", use_container_width=True):
        with st.spinner("🧠 Analyzing with AI..."):
            # Preprocess the image
            img_tensor = transform(image).unsqueeze(0).to(device)
            
            # Run inference
            with torch.no_grad():
                outputs = model(img_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted = torch.max(probabilities, 1)
            
            class_idx = predicted.item()
            class_name = CLASS_NAMES[class_idx]
            conf_score = round(confidence.item() * 100, 2)
            
            # Get recyclers
            recyclers = RECYCLERS.get(class_name, [])
            emoji = CLASS_EMOJIS.get(class_name, "♻️")
            
            # ========== DISPLAY RESULTS ==========
            st.markdown("---")
            
            # Top row
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.markdown(f'<div class="result-emoji">{emoji}</div>', unsafe_allow_html=True)
            
            with col2:
                label = class_name.replace("_", " ").title()
                st.markdown(f'<div class="result-label">{label}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-confidence">{conf_score}%</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-confidence-label">Confidence Score</div>', unsafe_allow_html=True)
            
            with col3:
                if conf_score >= 90:
                    badge = "🟢 High Confidence"
                    color = "#00f5a0"
                elif conf_score >= 70:
                    badge = "🟡 Medium Confidence"
                    color = "#f5a623"
                else:
                    badge = "🔴 Low Confidence"
                    color = "#ef4444"
                
                st.markdown(f"""
                <div style="
                    background: rgba(255,255,255,0.05);
                    border-radius: 12px;
                    padding: 1rem;
                    text-align: center;
                    border: 1px solid {color};
                    margin-top: 0.5rem;
                ">
                    <div style="color: {color}; font-weight: 700; font-size: 1.1rem;">{badge}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Progress bar
            st.progress(conf_score / 100)
            
            # Recyclers
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📍 Nearby Recycling Agents")
            
            if recyclers:
                for agent in recyclers:
                    st.markdown(f"""
                    <div class="recycler-card">
                        <div class="recycler-name">🏢 {agent['name']}</div>
                        <div class="recycler-address">📌 {agent['address']}</div>
                        <div class="recycler-distance">📏 {agent['distance']} away</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ No recycling agents found for this category in your area yet.")
            
            if conf_score >= 90:
                st.balloons()

st.markdown("""
<div class="footer">
    🌱 Built by <strong>Deneshwaran</strong>
</div>
""", unsafe_allow_html=True)
