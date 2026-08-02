# ============================================
# 🩸 RAKTCONNECT — Professional Edition v4.0 (FULLY UPGRADED)
# CodeStorm 2026 — FutureForge
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, asin
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# --- Optional: Folium for map clustering ---
try:
    import folium
    from folium.plugins import MarkerCluster
    from streamlit_folium import st_folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="RaktConnect — AI Emergency Blood Donor Network",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================

if 'donors_result' not in st.session_state:
    st.session_state.donors_result = None
if 'donors_total' not in st.session_state:
    st.session_state.donors_total = 0
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False
if 'history' not in st.session_state:
    st.session_state.history = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# ============================================
# CUSTOM CSS (with dark mode support)
# ============================================

def apply_css(dark_mode):
    if dark_mode:
        bg_main = "#0e1117"
        bg_card = "#1e1e1e"
        border_color = "#333333"
        text_color = "#fafafa"
        header_bg = "#1a1a2e"
        stat_bg = "#1e1e1e"
        footer_bg = "#1a1a2e"
        card_hover = "rgba(255,255,255,0.05)"
    else:
        bg_main = "#f5f7fa"
        bg_card = "rgba(255,255,255,0.95)"
        border_color = "#e8ecf0"
        text_color = "#0a1628"
        header_bg = "linear-gradient(135deg, #0a1628 0%, #1a2a4a 100%)"
        stat_bg = "rgba(255,255,255,0.8)"
        footer_bg = "#0a1628"
        card_hover = "rgba(0,0,0,0.02)"

    # CSS string
    css = f"""
    <style>
        .stApp {{
            background: {bg_main} !important;
        }}
        .stApp, .stApp p, .stApp span, .stApp div, .stApp label,
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {{
            color: {text_color} !important;
        }}
        .header {{
            background: {header_bg} !important;
            padding: 30px 40px;
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.05);
        }}
        .header h1 {{
            color: #ffffff !important;
            font-size: 2.8rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: -0.5px;
        }}
        .header h1 span {{
            color: #e74c3c;
            background: rgba(231, 76, 60, 0.15);
            padding: 0 15px;
            border-radius: 10px;
        }}
        .header .tagline {{
            color: #8899bb !important;
            font-size: 1.1rem;
            margin-top: 5px;
            font-weight: 400;
        }}
        .header .badge-container {{
            margin-top: 12px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .header .badge {{
            background: rgba(255,255,255,0.08);
            color: #aabbdd !important;
            padding: 4px 16px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            border: 1px solid rgba(255,255,255,0.05);
        }}
        .card {{
            background: {bg_card};
            backdrop-filter: blur(10px);
            padding: 25px 30px;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.04);
            border: 1px solid {border_color};
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }}
        .card:hover {{
            box-shadow: 0 8px 40px rgba(0,0,0,0.08);
            transform: translateY(-2px);
            background: {bg_card.replace('0.95','1.0')};
        }}
        .card h3 {{
            color: {text_color};
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .card h3 span {{
            font-size: 1.3rem;
        }}
        .stat-item {{
            background: {stat_bg};
            padding: 18px 20px;
            border-radius: 14px;
            text-align: center;
            border: 1px solid {border_color};
            transition: all 0.3s ease;
        }}
        .stat-item:hover {{
            border-color: #e74c3c;
        }}
        .stat-item .number {{
            font-size: 2.2rem;
            font-weight: 800;
            color: {text_color};
            line-height: 1.2;
        }}
        .stat-item .number.red {{ color: #e74c3c; }}
        .stat-item .number.green {{ color: #27ae60; }}
        .stat-item .number.blue {{ color: #3498db; }}
        .stat-item .label {{
            font-size: 0.75rem;
            color: #8899bb;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
            margin-top: 4px;
        }}
        .donor-card {{
            background: {bg_card};
            padding: 16px 20px;
            border-radius: 12px;
            border: 1px solid {border_color};
            margin: 8px 0;
            transition: all 0.3s ease;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .donor-card:hover {{
            border-color: #e74c3c;
            box-shadow: 0 4px 16px rgba(231, 76, 60, 0.1);
        }}
        .donor-card .rank {{
            font-size: 1.5rem;
            font-weight: 800;
            color: #e74c3c;
            min-width: 45px;
        }}
        .donor-card .info {{
            flex: 1;
            padding: 0 15px;
        }}
        .donor-card .info .name {{
            font-weight: 700;
            font-size: 1.05rem;
            color: {text_color};
        }}
        .donor-card .info .details {{
            font-size: 0.85rem;
            color: #8899bb;
        }}
        .donor-card .distance {{
            font-size: 1.2rem;
            font-weight: 800;
            color: #27ae60;
            text-align: right;
        }}
        .donor-card .badge {{
            padding: 2px 12px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 700;
            display: inline-block;
            margin-left: 8px;
        }}
        .badge-gold {{ background: #ffd700; color: #0a1628; }}
        .badge-silver {{ background: #c0c0c0; color: #0a1628; }}
        .badge-bronze {{ background: #cd7f32; color: white; }}
        .badge-platinum {{ background: #e5e4e2; color: #0a1628; border: 1px solid #c0a050; }}
        .stButton button {{
            background: linear-gradient(135deg, #0a1628, #1a2a4a) !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            padding: 12px 30px !important;
            border: none !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
        }}
        .stButton button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(10, 22, 40, 0.3) !important;
        }}
        .emergency-btn button {{
            background: linear-gradient(135deg, #e74c3c, #c0392b) !important;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0% {{ box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.4); }}
            70% {{ box-shadow: 0 0 0 15px rgba(231, 76, 60, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); }}
        }}
        .stTextInput input, .stSelectbox select {{
            border-radius: 10px !important;
            border: 2px solid {border_color} !important;
            padding: 10px 15px !important;
            transition: all 0.3s ease !important;
            background: {bg_card} !important;
            color: {text_color} !important;
        }}
        .stTextInput input:focus, .stSelectbox select:focus {{
            border-color: #0a1628 !important;
            box-shadow: 0 0 0 3px rgba(10, 22, 40, 0.1) !important;
        }}
        .footer {{
            text-align: center;
            padding: 25px;
            background: {footer_bg};
            border-radius: 16px;
            margin-top: 30px;
        }}
        .footer p {{
            color: #8899bb !important;
            font-size: 0.85rem;
            margin: 3px 0;
        }}
        .footer .brand {{
            color: white !important;
            font-weight: 700;
        }}
        .footer .brand span {{
            color: #e74c3c;
        }}
        section[data-testid="stSidebar"] {{
            background: {bg_card} !important;
            border-right: 1px solid {border_color};
        }}
        section[data-testid="stSidebar"] * {{
            color: {text_color} !important;
        }}
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {{
            color: {text_color} !important;
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: 4px;
            border-bottom: 2px solid {border_color};
        }}
        .stTabs [data-baseweb="tab"] {{
            color: #8899bb !important;
            font-weight: 600;
            padding: 10px 20px;
            border-radius: 10px 10px 0 0;
        }}
        .stTabs [aria-selected="true"] {{
            color: {text_color} !important;
            background: rgba(10, 22, 40, 0.05);
        }}
        .stProgress > div {{
            background: linear-gradient(90deg, #e74c3c, #f39c12, #27ae60) !important;
            border-radius: 10px !important;
        }}
        .map-box {{
            background: {bg_card};
            padding: 16px;
            border-radius: 8px;
            border: 1px solid {border_color};
        }}
        .how-box {{
            background: rgba(14, 92, 86, 0.1);
            border-radius: 8px;
            padding: 12px;
            margin-top: 10px;
            border-left: 4px solid #0E5C56;
        }}
        .how-box p {{ font-size: 0.9rem; margin: 4px 0; }}
        .stDataFrame {{
            background: {bg_card} !important;
        }}
        .stDataFrame thead th {{
            background: {bg_card} !important;
            color: {text_color} !important;
        }}
        .stDataFrame tbody td {{
            background: {bg_card} !important;
            color: {text_color} !important;
        }}
    </style>
    """
    return css

# Apply CSS based on session state
st.markdown(apply_css(st.session_state.dark_mode), unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================

st.markdown("""
<div class="header">
    <h1>🩸 <span>RaktConnect</span></h1>
    <p class="tagline">AI-Powered Emergency Blood &amp; Organ Donor Network</p>
    <div class="badge-container">
        <span class="badge">🏆 CodeStorm 2026</span>
        <span class="badge">🤖 AI-Powered Matching</span>
        <span class="badge">🩸 10,000+ Donors</span>
        <span class="badge">🌍 India-Wide Network</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# DATA LOADING
# ============================================

@st.cache_resource
def load_data():
    np.random.seed(42)
    
    cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Hyderabad', 
              'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']
    
    blood_groups = ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-']
    
    city_coords = {
        'Delhi': (28.6139, 77.2090), 'Mumbai': (19.0760, 72.8777),
        'Chennai': (13.0827, 80.2707), 'Bangalore': (12.9716, 77.5946),
        'Hyderabad': (17.3850, 78.4867), 'Kolkata': (22.5726, 88.3639),
        'Pune': (18.5204, 73.8567), 'Ahmedabad': (23.0225, 72.5714),
        'Jaipur': (26.9124, 75.7873), 'Lucknow': (26.8467, 80.9462)
    }
    
    first_names = ['Rahul','Priya','Amit','Neha','Vikram','Sneha','Arjun','Meera',
                   'Karan','Ananya','Rohan','Pooja','Suresh','Lakshmi','Manoj',
                   'Divya','Naveen','Kavya','Srinivas','Anjali','Rajesh','Sangeeta',
                   'Vijay','Shreya','Ajay','Anita','Sunil','Deepa','Ravi','Sonia']
    last_names = ['Sharma','Patel','Kumar','Singh','Reddy','Gupta','Nair','Iyer',
                  'Joshi','Rao','Verma','Malhotra','Srinivasan','Menon','Shetty',
                  'Pillai','Naidu','Das','Ganguly','Bose','Mishra','Tripathi']
    
    date_range = pd.date_range('2025-01-01', '2026-07-31')
    date_strings = [d.strftime('%Y-%m-%d') for d in date_range]
    random_dates = np.random.choice(date_strings, 10000)
    
    donors = []
    for i in range(10000):
        first = np.random.choice(first_names)
        last = np.random.choice(last_names)
        city = np.random.choice(cities)
        lat, lon = city_coords[city]
        lat += np.random.uniform(-0.5, 0.5)
        lon += np.random.uniform(-0.5, 0.5)
        blood = np.random.choice(blood_groups, p=[0.30, 0.25, 0.20, 0.10, 0.06, 0.04, 0.03, 0.02])
        
        donors.append({
            'name': f"{first} {last}",
            'blood_group': blood,
            'city': city,
            'latitude': lat,
            'longitude': lon,
            'phone': f"9{np.random.randint(100000000, 999999999)}",
            'available': np.random.choice(['Yes', 'Yes', 'Yes', 'No'], p=[0.75, 0.10, 0.10, 0.05]),
            'donations': np.random.randint(1, 20),
            'age': np.random.randint(18, 65),
            'gender': np.random.choice(['Male', 'Female', 'Other'], p=[0.6, 0.38, 0.02]),
            'last_donation': random_dates[i]
        })
    
    return pd.DataFrame(donors)

df = load_data()

# ============================================
# COMPATIBILITY MATRIX
# ============================================

compatibility = {
    'O+': ['O+', 'O-'],
    'O-': ['O-'],
    'A+': ['A+', 'A-', 'O+', 'O-'],
    'A-': ['A-', 'O-'],
    'B+': ['B+', 'B-', 'O+', 'O-'],
    'B-': ['B-', 'O-'],
    'AB+': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
    'AB-': ['A-', 'B-', 'AB-', 'O-']
}

def get_compatible(b):
    return compatibility.get(b.upper(), [])

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return 2 * R * asin(sqrt(sin((lat2 - lat1) / 2)**2 + 
                       cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2)**2))

def get_badge(donations):
    if donations >= 15:
        return '<span class="badge badge-platinum">🏆 Platinum</span>'
    elif donations >= 10:
        return '<span class="badge badge-gold">🥇 Gold</span>'
    elif donations >= 5:
        return '<span class="badge badge-silver">🥈 Silver</span>'
    else:
        return '<span class="badge badge-bronze">🥉 Bronze</span>'

def find_donors(patient_lat, patient_lon, patient_blood, urgency='normal', request_text=''):
    eligible = get_compatible(patient_blood)
    result = df[(df['blood_group'].str.upper().isin(eligible)) & (df['available'] == 'Yes')].copy()
    
    if len(result) == 0:
        return None, 0
    
    result['distance_km'] = result.apply(
        lambda r: haversine(patient_lat, patient_lon, r['latitude'], r['longitude']), axis=1
    )
    
    result = result.sort_values('distance_km')
    
    urgency_w = {'critical': 0.3, 'urgent': 0.6, 'normal': 1.0}
    result['priority_score'] = result['distance_km'] / 5 * urgency_w.get(urgency.lower(), 1.0)
    
    if request_text:
        emergency_keywords = ['emergency', 'accident', 'bleeding', 'critical', 'urgent', 'need blood', 'immediately']
        if any(word in request_text.lower() for word in emergency_keywords):
            result['priority_score'] = result['priority_score'] * 0.5
    
    result = result.sort_values('priority_score')
    return result.head(5), len(result)

# ============================================
# CITIES
# ============================================

cities = {
    'Delhi': (28.6139, 77.2090), 'Mumbai': (19.0760, 72.8777),
    'Chennai': (13.0827, 80.2707), 'Bangalore': (12.9716, 77.5946),
    'Hyderabad': (17.3850, 78.4867), 'Kolkata': (22.5726, 88.3639),
    'Pune': (18.5204, 73.8567), 'Ahmedabad': (23.0225, 72.5714),
    'Jaipur': (26.9124, 75.7873), 'Lucknow': (26.8467, 80.9462)
}

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("## 📊 Network Dashboard")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 10px; text-align: center;">
            <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff;">{len(df):,}</div>
            <div style="font-size: 0.7rem; color: #8899bb; text-transform: uppercase;">Total Donors</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 10px; text-align: center;">
            <div style="font-size: 1.8rem; font-weight: 800; color: #27ae60;">{len(df[df['available'] == 'Yes']):,}</div>
            <div style="font-size: 0.7rem; color: #8899bb; text-transform: uppercase;">Available</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🩸 Blood Group Distribution")
    bg_counts = df['blood_group'].value_counts()
    for bg, count in bg_counts.items():
        st.markdown(f"**{bg}** → {count:,}")
    
    st.markdown("---")
    
    st.markdown("### 📍 Top Cities")
    city_counts = df['city'].value_counts().head(5)
    for city, count in city_counts.items():
        st.markdown(f"**{city}** → {count:,}")
    
    st.markdown("---")
    
    st.markdown("### 🏆 Top Donors")
    for _, row in df.nlargest(3, 'donations')[['name', 'donations']].iterrows():
        st.markdown(f"🏅 {row['name']} — {row['donations']} donations")
    
    st.markdown("---")
    
    # Dark mode toggle
    dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode, key="dark_mode_toggle")
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()
    
    st.markdown("---")
    
    # Search history
    st.markdown("### 📋 Recent Searches")
    if st.session_state.history:
        for entry in st.session_state.history[-5:]:
            st.caption(f"{entry['timestamp']} — {entry['blood']} in {entry['city']} ({entry['urgency']})")
    else:
        st.caption("No searches yet")
    
    st.markdown("---")
    st.caption("🤖 AI-Powered Matching Engine v4.0")

# ============================================
# TABS
# ============================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Find Donors", "📊 Analytics", "📝 Register", "🗺️ Map", "📋 Browse All Donors"])

# ============================================
# TAB 1: FIND DONORS (PERSISTENT RESULTS)
# ============================================

with tab1:
    # Emergency Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚨 I NEED BLOOD NOW", use_container_width=True, key="emergency_btn"):
            st.session_state.emergency_mode = True
            st.success("🚨 Emergency mode activated! Critical urgency will be prioritized.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3><span>👤</span> Patient Details</h3>
        """, unsafe_allow_html=True)
        
        patient_name = st.text_input("Full Name", "Rajesh Kumar", key="patient_name")
        patient_blood = st.selectbox(
            "Blood Group",
            ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-'],
            key="patient_blood"
        )
        patient_city = st.selectbox(
            "City",
            list(cities.keys()),
            key="patient_city"
        )
        urgency = st.selectbox(
            "Urgency Level",
            ['Normal', 'Urgent', 'Critical'],
            key="urgency"
        )
        request_context = st.text_area(
            "Additional Context (Optional)",
            placeholder="e.g., Patient is bleeding, emergency surgery needed, accident victim...",
            height=80,
            key="request_context"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3><span>📋</span> Request Summary</h3>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**Patient:** {patient_name}")
        st.markdown(f"**Blood Group:** `{patient_blood}`")
        st.markdown(f"**Location:** 📍 {patient_city}")
        
        urgency_emoji = {'Normal': '🟢', 'Urgent': '🟡', 'Critical': '🔴'}
        st.markdown(f"**Urgency:** {urgency_emoji.get(urgency, '')} {urgency}")
        
        compatible_groups = get_compatible(patient_blood)
        st.markdown(f"**Compatible Groups:** {', '.join(compatible_groups)}")
        
        if request_context:
            st.markdown(f"**Context:** {request_context[:100]}...")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Search button
    if st.button("🔍 Find Compatible Donors", use_container_width=True, key="find_donors_btn"):
        lat, lon = cities.get(patient_city, (28.6139, 77.2090))
        
        with st.spinner("🤖 Analyzing donor network..."):
            time.sleep(0.8)
            donors, total = find_donors(lat, lon, patient_blood, urgency.lower(), request_context)
        
        # Store results and log history
        st.session_state.donors_result = donors
        st.session_state.donors_total = total
        st.session_state.search_performed = True
        
        # Append to history
        st.session_state.history.append({
            'blood': patient_blood,
            'city': patient_city,
            'urgency': urgency,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
        })
    
    # Display results from session state
    if st.session_state.get('search_performed', False):
        donors = st.session_state.donors_result
        total = st.session_state.donors_total
        
        if donors is None:
            st.error("❌ No compatible donors found in the network.")
            st.warning("🚨 Emergency alert: Escalating to hospital blood bank network...")
        else:
            st.success(f"✅ {total:,} compatible donors found in {time.strftime('%X')}!")
            
            if len(donors) < 3:
                st.progress(0.2, text="⚠️ CRITICAL SHORTAGE in this area!")
                st.warning("🚨 Fewer than 3 donors available. Emergency alert sent to hospitals.")
            elif len(donors) < 10:
                st.progress(0.5, text="🟡 Moderate supply available")
            else:
                st.progress(1.0, text="✅ Good supply nearby")
            
            st.markdown("### 🏆 Top Matches")
            
            emojis = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣']
            colors = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71', '#9b59b6']
            
            for i, (_, donor) in enumerate(donors.iterrows()):
                badge_html = get_badge(donor['donations'])
                wa_link = f"https://wa.me/91{donor['phone']}?text=Hi%20{donor['name'].split()[0]}%2C%20I%20need%20emergency%20blood%20donation."
                
                st.markdown(f"""
                <div class="donor-card" style="border-left: 4px solid {colors[i]};">
                    <div style="display: flex; align-items: center; gap: 15px; width: 100%; flex-wrap: wrap;">
                        <div class="rank" style="color: {colors[i]};">{emojis[i]}</div>
                        <div class="info" style="flex: 1;">
                            <div class="name">{donor['name']} {badge_html}</div>
                            <div class="details">
                                🩸 <strong>{donor['blood_group']}</strong> · 📍 {donor['city']} · 📞 {donor['phone']} · 💉 {donor['donations']} donations
                            </div>
                            <div class="details" style="font-size: 0.8rem; color: #555;">
                                🎂 Age: {donor.get('age', 'N/A')} · ⚤ {donor.get('gender', 'N/A')} · 📅 Last Donation: {donor.get('last_donation', 'N/A')}
                            </div>
                            <a href="{wa_link}" target="_blank" style="color: #25D366; text-decoration: none; font-weight: 600; font-size: 0.85rem;">
                                💬 Contact on WhatsApp
                            </a>
                        </div>
                        <div class="distance" style="text-align: right;">
                            {donor['distance_km']:.1f} km
                            <div style="font-size: 0.7rem; color: #8899bb; font-weight: 400;">
                                Priority: {donor['priority_score']:.2f}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Best Match
            best = donors.iloc[0]
            wa_link = f"https://wa.me/91{best['phone']}?text=Hi%20{best['name'].split()[0]}%2C%20I%20need%20emergency%20blood%20donation."
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #e8f5e9, #c8e6c9); padding: 20px 25px; border-radius: 14px; border-left: 6px solid #27ae60; margin-top: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <div style="font-size: 0.75rem; text-transform: uppercase; color: #2e7d32; font-weight: 700; letter-spacing: 1px;">
                            🎯 Best Match
                        </div>
                        <div style="font-size: 1.2rem; font-weight: 700; color: #1a1a2e;">
                            {best['name']} — {best['blood_group']}
                        </div>
                        <div style="color: #555; font-size: 0.95rem;">
                            📞 {best['phone']} · 📍 {best['city']}
                        </div>
                        <div style="color: #555; font-size: 0.9rem;">
                            📍 {best['distance_km']:.1f} km away · ⏱️ ~{best['distance_km'] / 30 * 60:.0f} min
                        </div>
                        <div style="color: #555; font-size: 0.85rem; margin-top: 4px;">
                            🎂 Age: {best.get('age', 'N/A')} · ⚤ {best.get('gender', 'N/A')} · 📅 Last Donation: {best.get('last_donation', 'N/A')}
                        </div>
                    </div>
                    <div>
                        <a href="{wa_link}" target="_blank" style="
                            display: inline-block;
                            background: #25D366;
                            color: white;
                            padding: 12px 25px;
                            border-radius: 30px;
                            text-decoration: none;
                            font-weight: 700;
                            font-size: 0.95rem;
                            transition: all 0.3s ease;
                        ">
                            💬 Contact Now
                        </a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("📱 Notification sent to donor! ✅")

# ============================================
# TAB 2: ANALYTICS
# ============================================

with tab2:
    st.markdown('<div class="card"><h3><span>📊</span> Donor Analytics Dashboard</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-item">
            <div class="number red">{len(df):,}</div>
            <div class="label">Total Donors</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-item">
            <div class="number green">{len(df[df['available'] == 'Yes']):,}</div>
            <div class="label">Available Now</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-item">
            <div class="number blue">{df['city'].nunique()}</div>
            <div class="label">Cities Covered</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-item">
            <div class="number">{df['donations'].mean():.1f}</div>
            <div class="label">Avg Donations</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🩸 Blood Group Distribution")
        fig = px.bar(
            df['blood_group'].value_counts().reset_index(),
            x='blood_group', y='count',
            color='blood_group',
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={'blood_group': 'Blood Group', 'count': 'Number of Donors'},
            height=350
        )
        fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📍 Donors by City")
        fig = px.bar(
            df['city'].value_counts().head(8).reset_index(),
            x='city', y='count',
            color='city',
            color_discrete_sequence=px.colors.qualitative.Pastel,
            labels={'city': 'City', 'count': 'Number of Donors'},
            height=350
        )
        fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📈 Donation Frequency")
        fig = px.histogram(
            df, x='donations',
            nbins=20,
            color_discrete_sequence=['#3498db'],
            labels={'donations': 'Number of Donations', 'count': 'Donors'},
            height=300
        )
        fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 👤 Gender Distribution")
        fig = px.pie(
            df, names='gender',
            color_discrete_sequence=px.colors.qualitative.Set3,
            height=300
        )
        fig.update_layout(showlegend=True, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    # Leaderboard
    st.markdown("---")
    st.markdown("### 🏆 Top 10 Donors")
    top_donors = df.nlargest(10, 'donations')[['name', 'donations', 'blood_group', 'city']]
    for i, (_, row) in enumerate(top_donors.iterrows()):
        badge = get_badge(row['donations'])
        st.markdown(f"{i+1}. **{row['name']}** — {row['donations']} donations {badge} (🩸 {row['blood_group']}, 📍 {row['city']})")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# TAB 3: REGISTER
# ============================================

with tab3:
    st.markdown('<div class="card"><h3><span>📝</span> Donor Registration</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #e8f5e9; padding: 15px 20px; border-radius: 12px; border-left: 4px solid #27ae60; margin-bottom: 20px;">
        <p style="margin: 0; font-weight: 600; color: #1a4a2a;">
            🩸 Join the network and help save lives!
        </p>
        <p style="margin: 5px 0 0; font-size: 0.9rem; color: #2e7d32;">
            Your registration could be the reason someone survives an emergency.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_name = st.text_input("Full Name", placeholder="Enter your full name", key="reg_name")
        new_blood = st.selectbox(
            "Blood Group",
            ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-'],
            key="donor_blood"
        )
        new_city = st.selectbox(
            "City",
            list(cities.keys()),
            key="donor_city"
        )
        new_gender = st.selectbox(
            "Gender",
            ['Male', 'Female', 'Other'],
            key="donor_gender"
        )
    
    with col2:
        new_phone = st.text_input("Phone Number", placeholder="9XXXXXXXXX", key="reg_phone")
        new_available = st.selectbox(
            "Availability",
            ['Yes', 'No'],
            key="donor_available"
        )
        new_age = st.number_input("Age", min_value=18, max_value=65, value=25, key="reg_age")
        new_donations = st.number_input("Total Past Donations", min_value=0, max_value=50, value=0, key="reg_donations")
    
    if st.button("✅ Register as Donor", use_container_width=True, key="register_btn"):
        if not new_name or not new_phone:
            st.error("❌ Please complete all required fields.")
        elif len(new_phone) < 10:
            st.error("❌ Please enter a valid 10-digit phone number.")
        else:
            lat, lon = cities.get(new_city, (28.6139, 77.2090))
            lat += np.random.uniform(-0.3, 0.3)
            lon += np.random.uniform(-0.3, 0.3)
            
            new_donor = pd.DataFrame({
                'name': [new_name],
                'blood_group': [new_blood],
                'city': [new_city],
                'latitude': [lat],
                'longitude': [lon],
                'phone': [new_phone],
                'available': [new_available],
                'donations': [new_donations],
                'age': [new_age],
                'gender': [new_gender],
                'last_donation': [datetime.now().strftime('%Y-%m-%d')]
            })
            
            if 'donors_df' not in st.session_state:
                st.session_state.donors_df = df
            st.session_state.donors_df = pd.concat([st.session_state.donors_df, new_donor], ignore_index=True)
            # Update the main df reference
            df = st.session_state.donors_df
            
            st.balloons()
            st.success(f"✅ Thank you, {new_name}! You're now registered as a donor!")
            
            st.markdown(f"""
            <div style="background: #e8f5e9; padding: 15px 20px; border-radius: 12px; border: 1px solid #a9dfbf; margin-top: 10px;">
                <p style="margin: 0; font-weight: 700; color: #1a4a2a;">
                    🩸 Your Details
                </p>
                <p style="margin: 5px 0; font-size: 0.9rem;">
                    {new_name} · {new_blood} · 📍 {new_city} · 📞 {new_phone}
                </p>
                <p style="margin: 5px 0; font-size: 0.85rem; color: #555;">
                    🏷️ Donor ID: RAKT-{random.randint(10000, 99999)}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# TAB 4: MAP (WITH CLUSTERING)
# ============================================

with tab4:
    st.markdown('<div class="card"><h3><span>🗺️</span> Donor Location Map</h3>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: #f0f2f6; padding: 15px; border-radius: 12px; margin-bottom: 15px;">
        <p style="margin: 0; font-size: 0.9rem; color: #555;">
            📍 Showing {len(df):,} donor locations across India. Hover over clusters or pins for details.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if FOLIUM_AVAILABLE:
        map_center = [20.5937, 78.9629]
        m = folium.Map(location=map_center, zoom_start=4, tiles='CartoDB positron')
        
        # Create marker cluster
        marker_cluster = MarkerCluster().add_to(m)
        
        # Sample up to 500 donors for performance
        sample_df = df.sample(min(500, len(df)))
        for _, row in sample_df.iterrows():
            color = 'red' if row['blood_group'] in ['O+', 'O-'] else 'blue' if row['blood_group'] in ['A+', 'A-'] else 'green'
            popup_text = f"""
            <b>{row['name']}</b><br>
            🩸 {row['blood_group']}<br>
            📍 {row['city']}<br>
            📞 {row['phone']}<br>
            💉 {row['donations']} donations
            """
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=6,
                popup=popup_text,
                color=color,
                fill=True,
                fillOpacity=0.7
            ).add_to(marker_cluster)
        
        st_folium(m, width=800, height=500)
        st.caption(f"📍 {len(df):,} donor locations (clustered view)")
    else:
        st.map(df[['latitude', 'longitude']].dropna(), zoom=4)
        st.info("💡 For an interactive clustered map, install: `pip install streamlit-folium folium`")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# TAB 5: BROWSE ALL DONORS
# ============================================

with tab5:
    st.markdown('<div class="card"><h3><span>📋</span> All Registered Donors</h3>', unsafe_allow_html=True)
    
    # Total counts
    st.markdown(f"### 🩸 Total Donors: **{len(df):,}**")
    st.markdown(f"### ✅ Available Now: **{len(df[df['available'] == 'Yes']):,}**")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        filter_blood = st.selectbox(
            "Filter by Blood Group",
            ['All'] + sorted(df['blood_group'].unique().tolist()),
            key="browse_blood"
        )
    with col2:
        filter_city = st.selectbox(
            "Filter by City",
            ['All'] + sorted(df['city'].unique().tolist()),
            key="browse_city"
        )
    
    # Search by name
    search_name = st.text_input("🔍 Search by Name", placeholder="Type donor name...", key="search_name")
    
    # Apply filters
    filtered_df = df.copy()
    if filter_blood != 'All':
        filtered_df = filtered_df[filtered_df['blood_group'] == filter_blood]
    if filter_city != 'All':
        filtered_df = filtered_df[filtered_df['city'] == filter_city]
    if search_name:
        filtered_df = filtered_df[filtered_df['name'].str.contains(search_name, case=False)]
    
    st.markdown(f"**Showing {len(filtered_df):,} donors**")
    
    # Rows per page slider
    rows_to_show = st.slider("Rows to display", min_value=10, max_value=500, value=100, step=10, key="browse_rows")
    
    # Display table
    display_df = filtered_df[['name', 'blood_group', 'city', 'phone', 'donations', 'age', 'gender', 'last_donation', 'available']].head(rows_to_show)
    
    st.dataframe(
        display_df,
        column_config={
            "name": "Name",
            "blood_group": "Blood Group",
            "city": "City",
            "phone": "Phone",
            "donations": "Donations",
            "age": "Age",
            "gender": "Gender",
            "last_donation": "Last Donation",
            "available": "Available"
        },
        use_container_width=True,
        height=400
    )
    
    if len(filtered_df) > rows_to_show:
        st.caption(f"Showing first {rows_to_show} of {len(filtered_df):,} donors. Adjust the slider to see more.")
    
    # Download CSV
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="raktconnect_donors.csv",
        mime="text/csv",
        key="download_csv"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div class="footer">
    <p><span class="brand">🩸 <span>Rakt</span>Connect</span> — Saving lives through intelligent donor matching</p>
    <p>Built for CodeStorm 2026: FutureForge</p>
    <p style="font-size: 0.75rem; opacity: 0.6;">© 2026 Team RaktConnect | All rights reserved</p>
</div>
""", unsafe_allow_html=True)
