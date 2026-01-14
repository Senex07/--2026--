import streamlit as st
import hashlib
import json
import random
from datetime import datetime
from fpdf import FPDF
import base64
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="🔮 العراف المغربي 2026",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load templates
@st.cache_data
def load_templates():
    try:
        with open('templates.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("فايل templates.json ملقاهوش. تاكد منو فالمكان الصحيح.")
        return {}

# Generate deterministic seed
def generate_seed(full_name, dob, city):
    input_string = f"{full_name}{dob}{city}"
    hash_object = hashlib.sha256(input_string.encode('utf-8'))
    return int(hash_object.hexdigest(), 16)

# Generate predictions
def generate_predictions(full_name, dob, city, templates, is_premium=False):
    seed = generate_seed(full_name, dob, city)
    random.seed(seed)
    
    predictions = {}
    used_indices = {}
    
    # Free sections
    for category in ['personality', 'prediction_2026']:
        if category in templates.get('free_sections', {}):
            items = templates['free_sections'][category]
            if items:
                index = random.randint(0, len(items) - 1)
                predictions[category] = items[index]
    
    # Premium sections
    if is_premium:
        for category in ['advice', 'warning', 'strength', 'lucky_number', 'lucky_day']:
            if category in templates.get('premium_sections', {}):
                items = templates['premium_sections'][category]
                if items:
                    index = random.randint(0, len(items) - 1)
                    predictions[category] = items[index]
    
    predictions['name'] = full_name
    predictions['dob'] = dob
    predictions['city'] = city
    predictions['generated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return predictions

# Create PDF export
def create_pdf(predictions, is_premium):
    pdf = FPDF()
    pdf.add_page()
    
    # Add custom font for Arabic (you need to add a font file)
    # For now using default font, but you can add Noto Naskh Arabic or similar
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="🔮 العراف المغربي 2026", ln=True, align='C')
    pdf.ln(10)
    
    # User info
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"الاسم: {predictions['name']}", ln=True, align='R')
    pdf.cell(200, 10, txt=f"تاريخ الميلاد: {predictions['dob']}", ln=True, align='R')
    pdf.cell(200, 10, txt=f"المدينة: {predictions['city']}", ln=True, align='R')
    pdf.ln(10)
    
    # Free sections
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="📜 شخصيتك فلمحة", ln=True, align='R')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=predictions.get('personality', ''), align='R')
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="🌟 توقعات 2026", ln=True, align='R')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=predictions.get('prediction_2026', ''), align='R')
    pdf.ln(5)
    
    # Premium sections
    if is_premium:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="💎 النصيحة الذهبية", ln=True, align='R')
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=predictions.get('advice', ''), align='R')
        pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="⚠️ انتباه مهم", ln=True, align='R')
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=predictions.get('warning', ''), align='R')
        pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="💪 نقطة القوة ديالك", ln=True, align='R')
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=predictions.get('strength', ''), align='R')
        pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="🔢 الحظ ديالك", ln=True, align='R')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"الرقم السعيد: {predictions.get('lucky_number', '')}", ln=True, align='R')
        pdf.cell(200, 10, txt=f"اليوم السعيد: {predictions.get('lucky_day', '')}", ln=True, align='R')
        pdf.ln(5)
    
    # Disclaimer
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 10, txt="⚠️ هاد المحتوى غير للترفيه والاستمتاع. لا يعتمد عليه في اتخاذ القرارات المهمة.", align='C')
    
    return pdf.output(dest='S').encode('latin1')

# Custom CSS for Moroccan theme
def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;500;600;700&display=swap');
        
        * {
            font-family: 'Noto Naskh Arabic', serif;
            text-align: right;
            direction: rtl;
        }
        
        /* Moroccan theme colors */
        :root {
            --moroccan-red: #C1272D;
            --moroccan-orange: #F7931E;
            --moroccan-yellow: #FFDE17;
            --moroccan-blue: #006233;
            --moroccan-green: #39B54A;
            --moroccan-gold: #D4AF37;
            --moroccan-dark: #8B4513;
        }
        
        .main-header {
            background: linear-gradient(135deg, var(--moroccan-red), var(--moroccan-orange));
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(193, 39, 45, 0.2);
        }
        
        .logo-area {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .stTextInput>div>div>input, .stDateInput>div>div>input {
            text-align: right;
            font-size: 16px;
            padding: 12px;
            border: 2px solid var(--moroccan-orange);
            border-radius: 10px;
            transition: all 0.3s;
        }
        
        .stTextInput>div>div>input:focus, .stDateInput>div>div>input:focus {
            border-color: var(--moroccan-red);
            box-shadow: 0 0 0 2px rgba(193, 39, 45, 0.2);
        }
        
        .stButton>button {
            background: linear-gradient(135deg, var(--moroccan-red), var(--moroccan-orange));
            color: white;
            font-size: 20px;
            font-weight: bold;
            border: none;
            border-radius: 50px;
            padding: 15px 40px;
            width: 100%;
            transition: all 0.3s;
            margin: 10px 0;
        }
        
        .stButton>button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(193, 39, 45, 0.3);
            background: linear-gradient(135deg, var(--moroccan-orange), var(--moroccan-red));
        }
        
        .prediction-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin: 15px 0;
            border-right: 6px solid var(--moroccan-gold);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s;
        }
        
        .prediction-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
        }
        
        .card-title {
            color: var(--moroccan-red);
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .card-content {
            color: #333;
            font-size: 18px;
            line-height: 1.8;
            padding-right: 10px;
        }
        
        .free-badge {
            background: var(--moroccan-green);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 10px;
        }
        
        .premium-badge {
            background: linear-gradient(135deg, var(--moroccan-gold), var(--moroccan-orange));
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 10px;
        }
        
        .action-buttons {
            display: flex;
            gap: 10px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .action-btn {
            background: var(--moroccan-blue);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 16px;
            flex: 1;
            text-align: center;
        }
        
        .action-btn:hover {
            background: var(--moroccan-green);
            transform: scale(1.05);
        }
        
        .premium-section {
            background: linear-gradient(135deg, #FFF8E1, #FFECB3);
            border: 2px solid var(--moroccan-gold);
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
        }
        
        .disclaimer-box {
            background: #F8F9FA;
            border-top: 3px solid var(--moroccan-red);
            padding: 20px;
            border-radius: 10px;
            margin-top: 40px;
            text-align: center;
        }
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .main-header {
                padding: 1.5rem;
            }
            
            .logo-area {
                font-size: 2rem;
            }
            
            .prediction-card {
                padding: 15px;
            }
            
            .card-title {
                font-size: 20px;
            }
            
            .card-content {
                font-size: 16px;
            }
            
            .stButton>button {
                padding: 12px 20px;
                font-size: 18px;
            }
        }
        
        /* Animation for cards */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .prediction-card {
            animation: fadeIn 0.5s ease-out;
        }
        
        /* Theme toggle */
        .theme-toggle {
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 1000;
        }
    </style>
    """, unsafe_allow_html=True)

# Copy to clipboard function
def copy_to_clipboard(text):
    components.html(
        f"""
        <script>
            navigator.clipboard.writeText(`{text}`);
        </script>
        """,
        height=0,
    )

def main():
    # Inject custom CSS
    inject_custom_css()
    
    # Load templates
    templates = load_templates()
    
    # Header with Moroccan design
    st.markdown("""
    <div class="main-header">
        <div class="logo-area">🔮</div>
        <h1 style="font-size: 2.5rem; margin: 0;">العراف المغربي 2026</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">توقعات شخصية بالدارجة المغربية</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Theme toggle (simplified)
    theme = st.sidebar.selectbox("الوضع", ["فاتح", "غامق"], index=0)
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 دخل معلوماتك")
        
        full_name = st.text_input(
            "الاسم الكامل",
            placeholder="اكتب الاسم الكامل ديالك",
            help="الاسم الكامل بالعربية أحسن"
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            dob = st.date_input(
                "تاريخ الميلاد",
                min_value=datetime(1900, 1, 1),
                max_value=datetime(2100, 12, 31)
            )
            dob_str = dob.strftime("%Y-%m-%d")
        
        with col_b:
            city = st.text_input(
                "مدينتك",
                placeholder="المدينة اللي كتعيش فيها",
                help="أي مدينة مغربية"
            )
    
    with col2:
        st.markdown("### ⭐ النسخة")
        is_premium = st.checkbox(
            "💎 نسخة كاملة",
            help="تحصل على كل التنبؤات (النصيحة، التحذير، القوة، والحظ)"
        )
        
        if is_premium:
            st.success("✅ نسخة كاملة مفعلة")
        else:
            st.info("🆓 النسخة المجانية: شخصيتك وتوقعات 2026 فقط")
    
    # Generate button
    if st.button("🔮 عطيني الرسالة ديالي", use_container_width=True):
        if full_name and city:
            # Generate predictions
            predictions = generate_predictions(full_name, dob_str, city, templates, is_premium)
            
            # Display predictions
            st.markdown("---")
            st.markdown(f'<h2 style="text-align: center; color: #C1272D;">الرسالة ديال {predictions["name"]}</h2>', unsafe_allow_html=True)
            
            # Free sections
            col1, col2 = st.columns(2)
            
            with col1:
                with st.container():
                    st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                    st.markdown('<span class="free-badge">🆓 مجاني</span>', unsafe_allow_html=True)
                    st.markdown('<div class="card-title">📜 شخصيتك فلمحة</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-content">{predictions.get("personality", "")}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                with st.container():
                    st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                    st.markdown('<span class="free-badge">🆓 مجاني</span>', unsafe_allow_html=True)
                    st.markdown('<div class="card-title">🌟 توقعات 2026</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-content">{predictions.get("prediction_2026", "")}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Premium sections
            if is_premium:
                st.markdown('<div class="premium-section">', unsafe_allow_html=True)
                st.markdown('<h3 style="color: #D4AF37; text-align: center;">💎 المحتوى الكامل</h3>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    with st.container():
                        st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                        st.markdown('<span class="premium-badge">💎 كامل</span>', unsafe_allow_html=True)
                        st.markdown('<div class="card-title">💎 النصيحة الذهبية</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="card-content">{predictions.get("advice", "")}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with st.container():
                        st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                        st.markdown('<span class="premium-badge">💎 كامل</span>', unsafe_allow_html=True)
                        st.markdown('<div class="card-title">💪 نقطة القوة ديالك</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="card-content">{predictions.get("strength", "")}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    with st.container():
                        st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                        st.markdown('<span class="premium-badge">💎 كامل</span>', unsafe_allow_html=True)
                        st.markdown('<div class="card-title">⚠️ انتباه مهم</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="card-content">{predictions.get("warning", "")}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with st.container():
                        st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                        st.markdown('<span class="premium-badge">💎 كامل</span>', unsafe_allow_html=True)
                        st.markdown('<div class="card-title">🍀 الحظ ديالك</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="card-content">')
                        st.markdown(f'<p><strong>🔢 الرقم السعيد:</strong> {predictions.get("lucky_number", "")}</p>')
                        st.markdown(f'<p><strong>📅 اليوم السعيد:</strong> {predictions.get("lucky_day", "")}</p>')
                        st.markdown('</div>')
                        st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Action buttons
            st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Copy to clipboard
                all_text = f"""الرسالة ديال {predictions['name']}
                
📜 شخصيتك فلمحة:
{predictions.get('personality', '')}

🌟 توقعات 2026:
{predictions.get('prediction_2026', '')}"""
                
                if is_premium:
                    all_text += f"""
                    
💎 النصيحة الذهبية:
{predictions.get('advice', '')}

⚠️ انتباه مهم:
{predictions.get('warning', '')}

💪 نقطة القوة ديالك:
{predictions.get('strength', '')}

🍀 الحظ ديالك:
الرقم السعيد: {predictions.get('lucky_number', '')}
اليوم السعيد: {predictions.get('lucky_day', '')}"""
                
                if st.button("📋 نسخ النص", use_container_width=True):
                    st.code(all_text)
                    st.success("✅ النص متاح للنسخ")
            
            with col2:
                # Export as PDF
                if st.button("📄 تصدير PDF", use_container_width=True):
                    pdf_data = create_pdf(predictions, is_premium)
                    
                    b64 = base64.b64encode(pdf_data).decode()
                    href = f'<a href="data:application/pdf;base64,{b64}" download="الرسالة_ديال_{predictions["name"]}_2026.pdf">⬇️ انقر هنا لتحميل PDF</a>'
                    st.markdown(href, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.error("⛔ من فضلك، دخل كل المعلومات المطلوبة")
    
    # Disclaimer
    st.markdown("---")
    st.markdown("""
    <div class="disclaimer-box">
        <h4>⚠️ تنبيه مهم</h4>
        <p>هاد المحتوى غير للترفيه والاستمتاع. لا يعتمد عليه في اتخاذ القرارات المهمة.</p>
        <p style="font-size: 0.9em; opacity: 0.7;">كل النصوص بالدارجة المغربية وتولد خوارزمياً</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>تم التطوير بكل ❤️ لخدمة الثقافة المغربية</p>
        <p>© 2024 العراف المغربي 2026 - نسخة 2.0</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
