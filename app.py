import streamlit as st
import hashlib
import json
import random
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="العراف المغربي 2026",
    page_icon="🔮",
    layout="centered"
)

# Custom CSS for styling 
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Noto Naskh Arabic', serif;
        text-align: right;
        direction: rtl;
    }
    
    .stButton > button {
        background-color: #8B4513;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px 24px;
        width: 100%;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #A0522D;
        transform: translateY(-2px);
    }
    
    .prediction-card {
        background-color: #FFF8DC;
        padding: 20px;
        border-radius: 15px;
        border-right: 5px solid #DAA520;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .prediction-title {
        color: #8B4513;
        font-weight: 700;
        font-size: 22px;
        margin-bottom: 10px;
        border-bottom: 2px solid #DAA520;
        padding-bottom: 5px;
    }
    
    .prediction-content {
        color: #2F4F4F;
        font-size: 18px;
        line-height: 1.6;
    }
    
    .main-title {
        text-align: center;
        color: #8B4513;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        text-align: center;
        color: #A0522D;
        font-size: 18px;
        margin-bottom: 40px;
    }
    
    .disclaimer {
        background-color: #F5F5F5;
        padding: 15px;
        border-radius: 10px;
        margin-top: 40px;
        text-align: center;
        font-size: 16px;
        color: #666;
        border-top: 2px solid #8B4513;
    }
    
    .lucky-section {
        display: flex;
        justify-content: space-around;
        background: linear-gradient(135deg, #8B4513 0%, #DAA520 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
    }
    
    .lucky-item {
        text-align: center;
    }
    
    .lucky-label {
        font-size: 16px;
        opacity: 0.9;
    }
    
    .lucky-value {
        font-size: 28px;
        font-weight: bold;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

def load_templates():
    """Load text templates from JSON file"""
    try:
        with open('templates.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("فايل templates.json ملقاهوش. تاكد منو فالمكان الصحيح.")
        return {}

def generate_seed(full_name, dob, city):
    """Generate a deterministic seed from user inputs"""
    input_string = f"{full_name}{dob}{city}"
    # Create hash
    hash_object = hashlib.sha256(input_string.encode('utf-8'))
    # Convert to integer for seed
    return int(hash_object.hexdigest(), 16)

def generate_predictions(full_name, dob, city, templates):
    """Generate all predictions based on inputs"""
    seed = generate_seed(full_name, dob, city)
    random.seed(seed)
    
    predictions = {}
    
    # Generate unique indices for each category
    used_indices = {}
    
    for category in ['personality', 'prediction_2026', 'strength', 'warning', 'advice', 'lucky_number', 'lucky_day']:
        if category in templates:
            category_items = templates[category]
            if category_items:
                # Generate unique index for this category
                index = random.randint(0, len(category_items) - 1)
                # Ensure no repetition within the same session
                while index in used_indices.get(category, []):
                    index = random.randint(0, len(category_items) - 1)
                
                used_indices.setdefault(category, []).append(index)
                predictions[category] = category_items[index]
    
    # Add personal touch
    predictions['name'] = full_name
    
    return predictions

def main():
    # Load templates
    templates = load_templates()
    if not templates:
        return
    
    # Header
    st.markdown('<h1 class="main-title">🔮 العراف المغربي 2026</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">دخل معلوماتك باش تعرف الرسالة الخاصة بيك ف2026</p>', unsafe_allow_html=True)
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        full_name = st.text_input("الاسم الكامل", placeholder="اكتب الاسم الكامل ديالك")
    
    with col2:
        dob = st.date_input("تاريخ الميلاد", min_value=datetime(1900, 1, 1))
        dob_str = dob.strftime("%Y-%m-%d")
    
    city = st.text_input("مدينتك", placeholder="اكتب المدينة اللي كتعيش فيها")
    
    # Generate button
    if st.button("عطيني الرسالة ديالي"):
        if full_name and city:
            # Generate predictions
            predictions = generate_predictions(full_name, dob_str, city, templates)
            
            # Display predictions
            st.markdown("---")
            st.markdown(f'<h2 style="text-align: center; color: #8B4513;">الرسالة ديال {predictions["name"]}</h2>', unsafe_allow_html=True)
            
            # Personality reading
            with st.container():
                st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                st.markdown('<div class="prediction-title">📜 شخصيتك فلمحة</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="prediction-content">{predictions["personality"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 2026 Prediction
            with st.container():
                st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                st.markdown('<div class="prediction-title">🌟 توقعات 2026</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="prediction-content">{predictions["prediction_2026"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Strength
            with st.container():
                st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                st.markdown('<div class="prediction-title">💪 نقطة القوة ديالك</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="prediction-content">{predictions["strength"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Warning
            with st.container():
                st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                st.markdown('<div class="prediction-title">⚠️ انتباه مهم</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="prediction-content">{predictions["warning"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Advice
            with st.container():
                st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                st.markdown('<div class="prediction-title">💎 النصيحة الذهبية</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="prediction-content">{predictions["advice"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Lucky numbers and days
            st.markdown('<div class="lucky-section">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="lucky-item">', unsafe_allow_html=True)
                st.markdown('<div class="lucky-label">🔢 الرقم السعيد</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="lucky-value">{predictions["lucky_number"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="lucky-item">', unsafe_allow_html=True)
                st.markdown('<div class="lucky-label">📅 اليوم السعيد</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="lucky-value">{predictions["lucky_day"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export option (simplified - in real app, you'd implement PDF generation)
            st.markdown("---")
            st.info("💡 يمكنك تصوير النتيجة أو حفظها كصورة لمراجعتها فيما بعد")
            
        else:
            st.warning("⛔ من فضلك، دخل كل المعلومات المطلوبة")
    
    # Disclaimer
    st.markdown("---")
    st.markdown('<div class="disclaimer">⚠️ هاد المحتوى غير للترفيه والاستمتاع. لا يعتمد عليه في اتخاذ القرارات المهمة.</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #666;'>تم التطوير بواسطة العراف المغربي 2026</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()