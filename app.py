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
    page_title="🔮 الرسائل الشخصية المغربية 2026",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load templates with caching
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

# Generate insights
def generate_insights(full_name, dob, city, templates, is_premium=False):
    seed = generate_seed(full_name, dob, city)
    random.seed(seed)
    
    insights = {}
    used_indices = {}
    
    # Helper function to get unique random item
    def get_unique_item(category, section_type='free_sections'):
        items = templates.get(section_type, {}).get(category, [])
        if not items:
            return ""
        
        max_retries = 10
        for _ in range(max_retries):
            index = random.randint(0, len(items) - 1)
            if index not in used_indices.get(category, []):
                used_indices.setdefault(category, []).append(index)
                return items[index]
        
        # If all indices used, return last one
        return items[-1]
    
    # Free sections
    insights['personality'] = get_unique_item('personality')
    insights['year_insight'] = get_unique_item('year_insight')
    
    # Premium sections
    if is_premium:
        premium_categories = [
            'golden_advice', 'warning_challenge', 'unexpected_opportunity',
            'monthly_activity', 'motivational_challenge', 'social_advice',
            'mini_quiz', 'moroccan_joke', 'motivational_phrase',
            'lucky_number', 'lucky_day'
        ]
        
        for category in premium_categories:
            insights[category] = get_unique_item(category, 'premium_sections')
    
    insights['name'] = full_name
    insights['dob'] = dob
    insights['city'] = city
    insights['generated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return insights

# Create PDF export
def create_pdf(insights, is_premium):
    pdf = FPDF()
    pdf.add_page()
    
    # Set font (using Arial as base, can be replaced with Arabic font)
    pdf.add_font('Arial', '', 'arial.ttf', uni=True)
    pdf.set_font('Arial', size=12)
    
    # Title
    pdf.set_font('Arial', 'B', 18)
    pdf.cell(200, 10, txt="🌿 الرسائل الشخصية المغربية 2026", ln=True, align='C')
    pdf.ln(10)
    
    # User info
    pdf.set_font('Arial', size=12)
    pdf.cell(200, 10, txt=f"الاسم: {insights['name']}", ln=True, align='R')
    pdf.cell(200, 10, txt=f"تاريخ الميلاد: {insights['dob']}", ln=True, align='R')
    pdf.cell(200, 10, txt=f"المدينة: {insights['city']}", ln=True, align='R')
    pdf.ln(15)
    
    # Free sections
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, txt="📜 نظرة على شخصيتك", ln=True, align='R')
    pdf.set_font('Arial', size=12)
    pdf.multi_cell(0, 10, txt=insights.get('personality', ''), align='R')
    pdf.ln(10)
    
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, txt="🌟 نظرة على عام 2026", ln=True, align='R')
    pdf.set_font('Arial', size=12)
    pdf.multi_cell(0, 10, txt=insights.get('year_insight', ''), align='R')
    pdf.ln(10)
    
    # Premium sections
    if is_premium:
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(200, 10, txt="💎 الإضافات الكاملة", ln=True, align='C')
        pdf.ln(5)
        
        premium_items = [
            ('💎 النصيحة الذهبية', 'golden_advice'),
            ('⚠️ تحدي وتحذير', 'warning_challenge'),
            ('🎯 فرصة غير متوقعة', 'unexpected_opportunity'),
            ('📅 نشاط مقترح للشهر', 'monthly_activity'),
            ('🏆 تحدي تحفيزي', 'motivational_challenge'),
            ('🤝 نصيحة للتفاعل الاجتماعي', 'social_advice')
        ]
        
        for title, key in premium_items:
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(200, 10, txt=title, ln=True, align='R')
            pdf.set_font('Arial', size=12)
            pdf.multi_cell(0, 10, txt=insights.get(key, ''), align='R')
            pdf.ln(5)
        
        # Fun sections
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(200, 10, txt="😄 فقرة ترفيهية", ln=True, align='R')
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(0, 10, txt=f"نكتة مغربية: {insights.get('moroccan_joke', '')}", align='R')
        pdf.ln(5)
        
        pdf.multi_cell(0, 10, txt=f"جملة تحفيزية: {insights.get('motivational_phrase', '')}", align='R')
        pdf.ln(5)
        
        # Lucky items
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(200, 10, txt="🍀 لمسات إضافية", ln=True, align='R')
        pdf.set_font('Arial', size=12)
        pdf.cell(200, 10, txt=f"الرقم السعيد: {insights.get('lucky_number', '')}", ln=True, align='R')
        pdf.cell(200, 10, txt=f"اليوم السعيد: {insights.get('lucky_day', '')}", ln=True, align='R')
        pdf.ln(10)
    
    # Disclaimer
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 10)
    pdf.multi_cell(0, 10, txt="⚠️ هاد المحتوى للترفيه فقط. الرسائل تولد خوارزمياً ولا تعتمد على أي مبادئ علمية أو تنبؤية.", align='C')
    
    return pdf.output(dest='S').encode('latin1')

# Inject custom CSS
def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');
        
        * {
            font-family: 'Noto Naskh Arabic', 'Amiri', serif;
            text-align: right;
            direction: rtl;
        }
        
        /* Moroccan color palette */
        :root {
            --moroccan-red: #C1272D;
            --moroccan-orange: #F7931E;
            --moroccan-yellow: #FFDE17;
            --moroccan-green: #39B54A;
            --moroccan-blue: #006233;
            --moroccan-gold: #D4AF37;
            --moroccan-dark: #8B4513;
            --moroccan-light: #FFF8E1;
        }
        
        /* Main header */
        .main-header {
            background: linear-gradient(135deg, var(--moroccan-red), var(--moroccan-orange), var(--moroccan-yellow));
            padding: 2.5rem;
            border-radius: 20px;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 40px rgba(193, 39, 45, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: "ⵣ";
            position: absolute;
            font-size: 300px;
            opacity: 0.1;
            top: -50px;
            right: -50px;
            transform: rotate(15deg);
        }
        
        .logo-area {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        /* Input styling */
        .stTextInput>div>div>input, .stDateInput>div>div>input {
            text-align: right;
            font-size: 18px;
            padding: 14px;
            border: 2px solid var(--moroccan-orange);
            border-radius: 12px;
            transition: all 0.3s;
            background: var(--moroccan-light);
        }
        
        .stTextInput>div>div>input:focus, .stDateInput>div>div>input:focus {
            border-color: var(--moroccan-red);
            box-shadow: 0 0 0 3px rgba(193, 39, 45, 0.3);
            background: white;
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(135deg, var(--moroccan-red), var(--moroccan-orange));
            color: white;
            font-size: 22px;
            font-weight: bold;
            border: none;
            border-radius: 60px;
            padding: 18px 50px;
            width: 100%;
            transition: all 0.4s;
            margin: 15px 0;
            position: relative;
            overflow: hidden;
        }
        
        .stButton>button:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(193, 39, 45, 0.4);
            background: linear-gradient(135deg, var(--moroccan-orange), var(--moroccan-red));
        }
        
        .stButton>button::after {
            content: "→";
            position: absolute;
            left: 30px;
            transition: transform 0.3s;
        }
        
        .stButton>button:hover::after {
            transform: translateX(-5px);
        }
        
        /* Cards styling */
        .insight-card {
            background: linear-gradient(145deg, #ffffff, #f8f8f8);
            border-radius: 18px;
            padding: 25px;
            margin: 18px 0;
            border-right: 8px solid var(--moroccan-gold);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
            transition: all 0.4s;
            position: relative;
            overflow: hidden;
        }
        
        .insight-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
        }
        
        .insight-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 5px;
            background: linear-gradient(90deg, var(--moroccan-red), var(--moroccan-orange), var(--moroccan-yellow));
        }
        
        .card-title {
            color: var(--moroccan-red);
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            gap: 12px;
            padding-right: 10px;
        }
        
        .card-content {
            color: #2c3e50;
            font-size: 19px;
            line-height: 1.9;
            padding-right: 15px;
            background: linear-gradient(45deg, transparent, rgba(255, 222, 23, 0.05));
            padding: 15px;
            border-radius: 10px;
        }
        
        /* Badges */
        .free-badge {
            background: linear-gradient(135deg, var(--moroccan-green), #27ae60);
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-size: 15px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 15px;
            box-shadow: 0 4px 15px rgba(57, 181, 74, 0.3);
        }
        
        .premium-badge {
            background: linear-gradient(135deg, var(--moroccan-gold), var(--moroccan-orange));
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-size: 15px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 15px;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
        }
        
        /* Premium section */
        .premium-section {
            background: linear-gradient(135deg, #FFF8E1, #FFECB3);
            border: 3px solid var(--moroccan-gold);
            padding: 25px;
            border-radius: 20px;
            margin: 25px 0;
            position: relative;
            overflow: hidden;
        }
        
        .premium-section::before {
            content: "💎";
            position: absolute;
            font-size: 200px;
            opacity: 0.05;
            bottom: -50px;
            right: -50px;
        }
        
        /* Action buttons */
        .action-buttons {
            display: flex;
            gap: 15px;
            margin-top: 25px;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .action-btn {
            background: linear-gradient(135deg, var(--moroccan-blue), #004d26);
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 18px;
            flex: 1;
            min-width: 200px;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .action-btn:hover {
            background: linear-gradient(135deg, var(--moroccan-green), #2ecc71);
            transform: scale(1.05);
            box-shadow: 0 8px 20px rgba(57, 181, 74, 0.3);
        }
        
        /* Fun highlights */
        .highlight-text {
            background: linear-gradient(45deg, transparent 40%, rgba(255, 222, 23, 0.2) 40%, rgba(255, 222, 23, 0.2) 60%, transparent 60%);
            padding: 2px 5px;
            border-radius: 4px;
        }
        
        /* Disclaimer */
        .disclaimer-box {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-top: 4px solid var(--moroccan-red);
            padding: 25px;
            border-radius: 15px;
            margin-top: 40px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        }
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .main-header {
                padding: 1.8rem;
                margin-bottom: 1.5rem;
            }
            
            .logo-area {
                font-size: 2.5rem;
            }
            
            .insight-card {
                padding: 18px;
                margin: 12px 0;
            }
            
            .card-title {
                font-size: 22px;
            }
            
            .card-content {
                font-size: 17px;
                line-height: 1.7;
            }
            
            .stButton>button {
                padding: 15px 25px;
                font-size: 20px;
            }
            
            .action-btn {
                padding: 12px 20px;
                font-size: 16px;
                min-width: 100%;
            }
            
            .action-buttons {
                flex-direction: column;
            }
        }
        
        /* Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .insight-card {
            animation: fadeInUp 0.6s ease-out;
        }
        
        /* Theme toggle */
        .theme-toggle {
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 1000;
            background: white;
            padding: 10px;
            border-radius: 50%;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            cursor: pointer;
        }
        
        /* Social sharing */
        .social-share {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 20px 0;
        }
        
        .social-icon {
            font-size: 24px;
            background: linear-gradient(135deg, var(--moroccan-red), var(--moroccan-orange));
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
            cursor: pointer;
        }
        
        .social-icon:hover {
            transform: scale(1.1);
            box-shadow: 0 8px 20px rgba(193, 39, 45, 0.3);
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Inject custom CSS
    inject_custom_css()
    
    # Load templates
    templates = load_templates()
    
    # Moroccan-themed header
    st.markdown("""
    <div class="main-header">
        <div class="logo-area">🌿✨</div>
        <h1 style="font-size: 3rem; margin: 10px 0; text-shadow: 2px 2px 8px rgba(0,0,0,0.3);">الرسائل الشخصية المغربية 2026</h1>
        <p style="font-size: 1.4rem; opacity: 0.95; margin-bottom: 10px;">رسائل شخصية تولد خصيصاً لك بالدارجة المغربية</p>
        <p style="font-size: 1rem; opacity: 0.8; background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; display: inline-block;">
            ⚠️ للترفيه فقط • تولد خوارزمياً • لا تعتمد على أي مبادئ علمية
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 أدخل معلوماتك الشخصية")
        
        full_name = st.text_input(
            "**الاسم الكامل**",
            placeholder="اكتب الاسم الكامل بالعربية",
            help="الاسم الكامل كما تحب أن يناديك به أحباؤك"
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            dob = st.date_input(
                "**تاريخ الميلاد**",
                min_value=datetime(1900, 1, 1),
                max_value=datetime(2100, 12, 31),
                help="اختر تاريخ ميلادك"
            )
            dob_str = dob.strftime("%Y-%m-%d")
        
        with col_b:
            city = st.text_input(
                "**مدينتك**",
                placeholder="المدينة التي تعيش فيها",
                help="أي مدينة مغربية أو عالمية"
            )
    
    with col2:
        st.markdown("### ⭐ اختر النسخة")
        
        is_premium = st.checkbox(
            "💎 **النسخة الكاملة**",
            help="تحصل على كل الرسائل: نصائح، تحذيرات، فرص، نشاطات، وتحديات"
        )
        
        if is_premium:
            st.success("""
            **✅ النسخة الكاملة مفعلة!**
            
            ستتلقى:
            • النصيحة الذهبية
            • التحدي والتحذير
            • الفرصة غير المتوقعة
            • نشاط مقترح للشهر
            • تحدي تحفيزي
            • نكتة مغربية
            • والمزيد...
            """)
        else:
            st.info("""
            **🆓 النسخة المجانية**
            
            تحصل على:
            • نظرة على شخصيتك
            • نظرة على عام 2026
            """)
        
        # Social sharing
        st.markdown("### 🤝 شارك التطبيق")
        st.markdown("""
        <div class="social-share">
            <div class="social-icon" onclick="navigator.share({title: 'الرسائل الشخصية المغربية', text: 'جرب تطبيق الرسائل الشخصية المغربية 2026!', url: window.location.href})">📱</div>
            <div class="social-icon" onclick="window.open('https://wa.me/?text=' + encodeURIComponent('جرب تطبيق الرسائل الشخصية المغربية 2026! ' + window.location.href))">💬</div>
            <div class="social-icon" onclick="window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent('جرب تطبيق الرسائل الشخصية المغربية 2026! ' + window.location.href))">🐦</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Generate button
    if st.button("✨ عطيني الرسالة ديالي", use_container_width=True, type="primary"):
        if full_name and city:
            # Generate insights
            insights = generate_insights(full_name, dob_str, city, templates, is_premium)
            
            # Display insights
            st.markdown("---")
            st.markdown(f'<h2 style="text-align: center; color: #C1272D; margin-bottom: 30px;">🌿 رسائل خاصة لـ {insights["name"]}</h2>', unsafe_allow_html=True)
            
            # Free sections
            col1, col2 = st.columns(2)
            
            with col1:
                with st.container():
                    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
                    st.markdown('<span class="free-badge">🆓 نسخة مجانية</span>', unsafe_allow_html=True)
                    st.markdown('<div class="card-title">📜 نظرة على شخصيتك</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-content">{insights.get("personality", "")}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                with st.container():
                    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
                    st.markdown('<span class="free-badge">🆓 نسخة مجانية</span>', unsafe_allow_html=True)
                    st.markdown('<div class="card-title">🌟 نظرة على عام 2026</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-content">{insights.get("year_insight", "")}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Premium sections
            if is_premium:
                st.markdown('<div class="premium-section">', unsafe_allow_html=True)
                st.markdown('<h2 style="color: #D4AF37; text-align: center; margin-bottom: 25px;">💎 الإضافات الكاملة</h2>', unsafe_allow_html=True)
                
                # First row
                col1, col2 = st.columns(2)
                
                with col1:
                    with st.container():
                        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
                        st.markdown('<span class="premium-badge">💎 كامل</span>', unsafe_allow_html=True)
                        st.markdown('<div class="card-title">💎 النصيحة الذهبية</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="card-content">{insights.get("golden_advice", "")}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with st.container():
                        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
                        st.markdown('<span class="premium-badge">💎 كامل</span>', unsafe_allow_html=True)
                        st.markdown('<div class="card-title">⚠️ تحدي وتحذير</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="card-content">{insights.get("warning_challenge", "")}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    with st.container():
                        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
                        st.markdown('<span class="premium-badge">💎 كامل</span>', unsafe_allow_html=True)
                        st.markdown('<div class="card-title">🎯 فرصة غير متوقعة</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="card-content">{insights.get("unexpected_opportunity", "")}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with st.container():
                        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
                        st.markdown('<span class="premium-badge">💎 كامل</span>', unsafe_allow_html=True)
                        st.markdown('<div class="card-title">📅 نشاط للشهر</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="card-content">{insights.get("monthly_activity", "")}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                
                # Second row
                col1, col2 = st.columns(2)
                
                with col1:
                    with st.container():
                        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
                        st.markdown('<span class="premium-badge">💎 كامل</span>', unsafe_allow_html=True)
                        st.markdown('<div class="card-title">🏆 تحدي تحفيزي</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="card-content">{insights.get("motivational_challenge", "")}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with st.container():
                        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
                        st.markdown('<span class="premium-badge">💎 كامل</span>', unsafe_allow_html=True)
                        st.markdown('<div class="card-title">🤝 نصيحة اجتماعية</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="card-content">{insights.get("social_advice", "")}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    with st.container():
                        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
                        st.markdown('<span class="premium-badge">💎 كامل</span>', unsafe_allow_html=True)
                        st.markdown('<div class="card-title">😄 نكتة مغربية</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="card-content">{insights.get("moroccan_joke", "")}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with st.container():
                        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
                        st.markdown('<span class="premium-badge">💎 كامل</span>', unsafe_allow_html=True)
                        st.markdown('<div class="card-title">✨ لمسات إضافية</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="card-content">')
                        st.markdown(f'<p><strong>🔢 الرقم السعيد:</strong> {insights.get("lucky_number", "")}</p>')
                        st.markdown(f'<p><strong>📅 اليوم السعيد:</strong> {insights.get("lucky_day", "")}</p>')
                        st.markdown(f'<p><strong>💬 جملة تحفيزية:</strong> {insights.get("motivational_phrase", "")}</p>')
                        st.markdown('</div>')
                        st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Action buttons
            st.markdown("---")
            st.markdown('<h3 style="text-align: center; color: #006233;">📤 مشاركة وحفظ الرسائل</h3>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Copy to clipboard
                all_text = f"""🌿 الرسائل الشخصية لـ {insights['name']}
                
📜 نظرة على شخصيتك:
{insights.get('personality', '')}

🌟 نظرة على عام 2026:
{insights.get('year_insight', '')}"""
                
                if is_premium:
                    all_text += f"""
                    
💎 الإضافات الكاملة:
💎 النصيحة الذهبية: {insights.get('golden_advice', '')}
⚠️ تحدي وتحذير: {insights.get('warning_challenge', '')}
🎯 فرصة غير متوقعة: {insights.get('unexpected_opportunity', '')}
📅 نشاط للشهر: {insights.get('monthly_activity', '')}
🏆 تحدي تحفيزي: {insights.get('motivational_challenge', '')}
🤝 نصيحة اجتماعية: {insights.get('social_advice', '')}
😄 نكتة مغربية: {insights.get('moroccan_joke', '')}
✨ لمسات إضافية:
   • الرقم السعيد: {insights.get('lucky_number', '')}
   • اليوم السعيد: {insights.get('lucky_day', '')}
   • جملة تحفيزية: {insights.get('motivational_phrase', '')}"""
                
                if st.button("📋 نسخ النص", use_container_width=True):
                    st.code(all_text)
                    st.success("✅ تم نسخ النص بنجاح! يمكنك لصقه في أي مكان.")
            
            with col2:
                # Export as PDF
                if st.button("📄 تصدير PDF", use_container_width=True):
                    pdf_data = create_pdf(insights, is_premium)
                    
                    b64 = base64.b64encode(pdf_data).decode()
                    href = f'<a href="data:application/pdf;base64,{b64}" download="الرسائل_الشخصية_{insights["name"]}_2026.pdf" style="text-decoration: none; color: white;">⬇️ تحميل PDF</a>'
                    st.markdown(f"""
                    <div style="text-align: center; padding: 10px;">
                        {href}
                    </div>
                    """, unsafe_allow_html=True)
            
            with col3:
                # Share button
                if st.button("📤 مشاركة", use_container_width=True):
                    share_text = f"جربت تطبيق الرسائل الشخصية المغربية 2026 وحصلت على رسائل شخصية رائعة!"
                    st.markdown(f"""
                    <div style="text-align: center; padding: 10px;">
                        <p>شارك عبر:</p>
                        <div class="social-share">
                            <div class="social-icon" onclick="navigator.share({{title: 'رسائلي الشخصية', text: '{share_text}', url: window.location.href}})">📱</div>
                            <div class="social-icon" onclick="window.open('https://wa.me/?text=' + encodeURIComponent('{share_text} ' + window.location.href))">💬</div>
                            <div class="social-icon" onclick="window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent('{share_text} ' + window.location.href))">🐦</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
        else:
            st.error("⛔ من فضلك، أدخل كل المعلومات المطلوبة")
    
    # Disclaimer and legal text
    st.markdown("---")
    st.markdown("""
    <div class="disclaimer-box">
        <h4>📜 ملاحظات قانونية وأخلاقية</h4>
        <p><strong>⚠️ هاد المحتوى للترفيه فقط:</strong> كل الرسائل تولد خوارزمياً باستخدام Python ولا تعتمد على أي مبادئ علمية، تنبؤية، فلكية، أو روحية.</p>
        <p><strong>🔒 خصوصيتك محمية:</strong> لا يتم حفظ أو تخزين أو مشاركة أي من معلوماتك الشخصية. كل العمليات تجري محلياً على جهازك.</p>
        <p><strong>🎯 الغرض من التطبيق:</strong> تقديم رسائل إيجابية وتحفيزية باللهجة المغربية للترفيه والتشجيع فقط.</p>
        <p><strong>🚫 لا للاعتماد:</strong> لا تعتمد على هذه الرسائل لأخذ قرارات مهمة في حياتك، العمل، الصحة، أو العلاقات.</p>
        <p style="font-size: 0.9em; margin-top: 15px; opacity: 0.7;">© 2024 الرسائل الشخصية المغربية - تطوير تقني للترفيه الإيجابي</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 25px;">
        <p style="font-size: 1.1em;">🌿 تم التطوير بكل ❤️ لخدمة الثقافة واللغة المغربية</p>
        <p style="font-size: 0.9em; opacity: 0.8;">استمتع برسائل إيجابية وترفيهية بالدارجة المغربية المحببة</p>
        <p style="margin-top: 20px; font-size: 0.8em; opacity: 0.6;">الإصدار 3.0 | يدعم جميع الأجهزة | تصميم مغربي أصيل</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
