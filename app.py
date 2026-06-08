"""
Main Streamlit Application for Mohenjo-Daro Heritage Chatbot
Complete with Gemini LLM and Image Gallery
"""
import streamlit as st
import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from utils.chatbot import HeritageChatbot
from utils.image_gen import ImageGenerator
from utils.knowledge_base import kb

# Page configuration
st.set_page_config(
    page_title="Mohenjo-Daro Heritage AI Chatbot",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,215,0,0.3);
    }
    .main-header h1 {
        color: #ffd700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .image-triggered {
        background: linear-gradient(135deg, #27ae60, #2ecc71);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        color: white;
        font-size: 0.8rem;
        display: inline-block;
        margin-top: 0.5rem;
    }
    .info-card {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 1.2rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .success-badge {
        background: #27ae60;
        color: white;
        padding: 0.5rem;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
    }
    .stButton > button {
        background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(243,156,18,0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False

if not st.session_state.initialized:
    try:
        st.session_state.chatbot = HeritageChatbot()
        st.session_state.chatbot_ready = True
    except Exception as e:
        st.session_state.chatbot = None
        st.session_state.chatbot_ready = False
        st.session_state.chatbot_error = str(e)
    
    st.session_state.image_gen = ImageGenerator()
    st.session_state.messages = []
    st.session_state.generated_images = {}
    st.session_state.sample_qa = None
    st.session_state.initialized = True

# Function to check if question is asking for images
def wants_image(question):
    visual_keywords = [
        'image', 'picture', 'photo', 'show me', 'visual',
        'what did it look like', 'appearance', 'see', 'view',
        'generate', 'display', 'how did it look', 'reconstruction',
        'what it looked like', 'illustration', 'depict', 'draw',
        'show', 'look like', 'looked like'
    ]
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in visual_keywords)

# Function to get image based on question topic
def get_image_for_question(question):
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['bath', 'pool', 'water', 'ritual']):
        return "great_bath", "🛁 The Great Bath - Ancient Ritual Pool"
    elif any(word in question_lower for word in ['street', 'urban', 'planning', 'grid', 'drain']):
        return "architecture", "🏗️ Urban Planning - Grid Streets & Drainage"
    elif any(word in question_lower for word in ['overview', 'aerial', 'full', 'entire', 'whole city']):
        return "overview", "🏛️ Mohenjo-Daro - Complete City View"
    elif any(word in question_lower for word in ['look', 'past', 'ancient', 'reconstruct', 'appearance']):
        return "overview", "🏛️ Mohenjo-Daro - Ancient City Reconstruction"
    elif any(word in question_lower for word in ['house', 'home', 'building', 'brick']):
        return "architecture", "🏗️ Residential Buildings & Architecture"
    else:
        return "overview", "🏛️ Mohenjo-Daro Heritage Site"

# Function to load images if not already loaded
def ensure_images_loaded():
    if not st.session_state.generated_images:
        try:
            images, image_map = st.session_state.image_gen.generate_project_images()
            if image_map:
                st.session_state.generated_images = image_map
                return True
        except:
            # Fallback: try old method
            try:
                images = st.session_state.image_gen.generate_project_images()
                if images:
                    if len(images) >= 1:
                        st.session_state.generated_images["great_bath"] = images[0]
                    if len(images) >= 2:
                        st.session_state.generated_images["architecture"] = images[1]
                    if len(images) >= 3:
                        st.session_state.generated_images["overview"] = images[2]
                    return True
            except:
                pass
    return len(st.session_state.generated_images) > 0

# Header
st.markdown("""
<div class="main-header">
    <h1>🏛️ Mohenjo-Daro Heritage AI Chatbot</h1>
    <h3>🤖 Powered by Google Gemini 2.5 Flash</h3>
    <p>Explore the Ancient Indus Valley Civilization | UNESCO World Heritage Site | 2500 BCE</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">📍 Larkana District, Sindh, Pakistan</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🏺 Site Information")
    st.markdown(f"""
    <div class="info-card">
    📍 <b>Site:</b> {kb.site_name}<br>
    🗺️ <b>Location:</b> {kb.location}<br>
    📅 <b>Period:</b> 2500-1900 BCE<br>
    🏆 <b>Status:</b> UNESCO World Heritage (1980)<br>
    🔍 <b>Discovered:</b> 1922 by R.D. Banerji<br>
    🤖 <b>AI Model:</b> Google Gemini 2.5 Flash
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # API Status
    if st.session_state.chatbot_ready:
        st.markdown('<div class="success-badge">✅ Gemini API Connected</div>', unsafe_allow_html=True)
    else:
        st.error(f"⚠️ API Error: {st.session_state.get('chatbot_error', 'Check your .env file')}")
    
    st.markdown("---")
    st.markdown("## 🎨 Image Gallery")
    
    if st.button("🖼️ Load All Heritage Images", use_container_width=True):
        with st.spinner("📥 Downloading Mohenjo-Daro heritage images..."):
            if ensure_images_loaded():
                st.success(f"✅ {len(st.session_state.generated_images)} images loaded!")
                st.balloons()
            else:
                st.error("❌ Failed to load images. Check internet connection.")
    
    if st.session_state.generated_images:
        st.info(f"📸 {len(st.session_state.generated_images)} images available")
    else:
        st.warning("⚠️ Click 'Load All Heritage Images' button above first!")
    
    st.markdown("---")
    st.markdown("## 💡 Try These Visual Questions:")
    
    visual_questions = [
        "Show me the Great Bath",
        "What did the ancient city look like?",
        "Show me the urban planning of Mohenjo-Daro",
        "Display a picture of the city overview",
        "Show me what houses looked like",
        "Generate an image of the Great Bath"
    ]
    
    for i, q in enumerate(visual_questions):
        if st.button(f"🖼️ {q}", use_container_width=True, key=f"vis_{i}"):
            st.session_state.pending_question = q

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 💬 Chat with Your AI Archaeologist")
    st.markdown("*Ask me anything about Mohenjo-Daro! Try asking for images!*")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # Show image if message has one
            if message.get("image_path") and os.path.exists(message["image_path"]):
                st.image(message["image_path"], use_container_width=True)
                st.markdown(f'<div class="image-triggered">🖼️ {message.get("image_caption", "")}</div>', 
                          unsafe_allow_html=True)
    
    # Handle pending question from sidebar
    if 'pending_question' in st.session_state:
        prompt = st.session_state.pending_question
        del st.session_state.pending_question
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            if st.session_state.chatbot_ready:
                with st.spinner("🤔 Researching Mohenjo-Daro archives..."):
                    try:
                        response = st.session_state.chatbot.get_response(prompt)
                        st.markdown(response)
                        
                        msg_data = {"role": "assistant", "content": response}
                        
                        # Check if user wants an image
                        if wants_image(prompt):
                            # Ensure images are loaded
                            ensure_images_loaded()
                            
                            img_key, img_caption = get_image_for_question(prompt)
                            if img_key in st.session_state.generated_images:
                                img_path = st.session_state.generated_images[img_key]
                                if os.path.exists(img_path):
                                    msg_data["image_path"] = img_path
                                    msg_data["image_caption"] = img_caption
                                    st.image(img_path, use_container_width=True)
                                    st.markdown(f'<div class="image-triggered">🖼️ {img_caption}</div>', 
                                              unsafe_allow_html=True)
                                else:
                                    st.warning(f"Image file not found: {img_path}")
                            else:
                                st.warning(f"No image for key: {img_key}. Available: {list(st.session_state.generated_images.keys())}")
                        
                        st.session_state.messages.append(msg_data)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.error("Chatbot not available. Check your API key.")
        st.rerun()
    
    # Chat input
    if prompt := st.chat_input("Ask about Mohenjo-Daro (try: 'Show me the Great Bath')..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            if st.session_state.chatbot_ready:
                with st.spinner("🤔 Researching Mohenjo-Daro archives..."):
                    try:
                        response = st.session_state.chatbot.get_response(prompt)
                        st.markdown(response)
                        
                        msg_data = {"role": "assistant", "content": response}
                        
                        # Auto-generate image for visual questions
                        if wants_image(prompt):
                            ensure_images_loaded()
                            
                            img_key, img_caption = get_image_for_question(prompt)
                            if img_key in st.session_state.generated_images:
                                img_path = st.session_state.generated_images[img_key]
                                if os.path.exists(img_path):
                                    msg_data["image_path"] = img_path
                                    msg_data["image_caption"] = img_caption
                                    st.image(img_path, use_container_width=True)
                                    st.markdown(f'<div class="image-triggered">🖼️ {img_caption}</div>', 
                                              unsafe_allow_html=True)
                                else:
                                    st.warning(f"Image file not found")
                            else:
                                st.info(f"💡 Available images: {list(st.session_state.generated_images.keys())}")
                        
                        st.session_state.messages.append(msg_data)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.error("Chatbot not available. Check API key.")

with col2:
    st.markdown("## 🖼️ Image Gallery")
    
    if st.session_state.generated_images:
        for img_key, img_path in st.session_state.generated_images.items():
            if os.path.exists(img_path):
                captions = {
                    "great_bath": "🛁 The Great Bath - 12m x 7m Ritual Pool",
                    "architecture": "🏗️ Urban Architecture & Grid Streets",
                    "overview": "🏛️ Mohenjo-Daro City Overview"
                }
                st.image(img_path, use_container_width=True)
                st.caption(captions.get(img_key, img_key))
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2c3e50, #34495e); 
                    padding: 2rem; border-radius: 10px; text-align: center; color: white;
                    border: 2px dashed rgba(255,215,0,0.3);">
            <h2>🏛️</h2>
            <h4>No Images Loaded Yet</h4>
            <p style="font-size: 0.9rem;">👆 Click <b>'Load All Heritage Images'</b> in sidebar</p>
            <p style="font-size: 0.8rem; opacity: 0.7;">OR ask a visual question like:</p>
            <p style="font-size: 0.8rem; color: #ffd700;">'Show me the Great Bath'</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 📋 Sample Q&A (Project Requirement)")
    
    with st.expander("📖 Click to view 5 Sample Questions & Answers", expanded=False):
        if st.button("🔄 Generate Sample Q&A", use_container_width=True):
            if st.session_state.chatbot_ready:
                with st.spinner("Generating sample questions and answers..."):
                    st.session_state.sample_qa = st.session_state.chatbot.get_sample_qa()
                    st.success("✅ Sample Q&A generated!")
            else:
                st.error("❌ Chatbot not available")
        
        if st.session_state.sample_qa:
            for i, qa in enumerate(st.session_state.sample_qa, 1):
                st.markdown(f"### Q{i}: {qa['question']}")
                st.markdown(f"**Answer:** {qa['answer']}")
                st.markdown("---")
        else:
            st.info("Click 'Generate Sample Q&A' button above")

# Footer
st.markdown("---")
st.markdown("""
<footer style='text-align: center; color: #95a5a6;'>
    <b>🎓 Semester Project | Mohenjo-Daro Heritage AI Chatbot</b><br>
    Site: Mohenjo-Daro, Pakistan | AI: Google Gemini 2.5 Flash<br>
    📅 Presentation: May 13, 2026
</footer>
""", unsafe_allow_html=True)