# ============================================
# RaktConnect — Premium Edition
# CodeStorm 2026 — FutureForge
# ============================================
import google.generativeai as genai
import streamlit as st
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, asin
import time

st.set_page_config(
    page_title="RaktConnect — Emergency Blood Donor Network",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SESSION STATE
# ============================================

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Initialize chat history for AI assistant
if 'ai_chat_history' not in st.session_state:
    st.session_state.ai_chat_history = []

# ============================================
# PREMIUM CSS — Glassmorphism + Gradients + Animations
# ============================================

def apply_css(dark_mode):
    if dark_mode:
        bg_main = "#0b0e14"
        bg_card = "rgba(255,255,255,0.06)"
        border_color = "rgba(255,255,255,0.08)"
        text_color = "#f0f4fa"
        header_bg = "linear-gradient(135deg, #0d1b2a, #1b3a5c)"
        stat_bg = "rgba(255,255,255,0.04)"
        footer_bg = "rgba(0,0,0,0.3)"
        shadow = "0 8px 32px rgba(0,0,0,0.4)"
        glass = "backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);"
    else:
        bg_main = "#f0f4fa"
        bg_card = "rgba(255,255,255,0.7)"
        border_color = "rgba(255,255,255,0.3)"
        text_color = "#0a1628"
        header_bg = "linear-gradient(135deg, #0a1628, #1a3a6a, #2d5a8a)"
        stat_bg = "rgba(255,255,255,0.5)"
        footer_bg = "rgba(255,255,255,0.8)"
        shadow = "0 8px 32px rgba(0,0,0,0.08)"
        glass = "backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);"

    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            transition: background 0.3s ease, color 0.2s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        }}

        .stApp {{
            background: {bg_main} !important;
            font-family: 'Inter', sans-serif;
        }}

        .stApp, .stApp p, .stApp span, .stApp div, .stApp label,
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {{
            color: {text_color};
            font-family: 'Inter', sans-serif;
        }}

        .block-container {{
            max-width: 1200px;
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }}

        /* ---- GLASS HEADER ---- */
        .header {{
            background: {header_bg};
            padding: 2rem 2.5rem;
            border-radius: 24px;
            margin-bottom: 2rem;
            box-shadow: 0 12px 48px rgba(0,0,0,0.15);
            border: 1px solid rgba(255,255,255,0.1);
            position: relative;
            overflow: hidden;
        }}
        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(255,255,255,0.08), transparent 70%);
            border-radius: 50%;
            pointer-events: none;
        }}
        .header h1 {{
            font-size: 2.8rem;
            font-weight: 900;
            color: #ffffff !important;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .header h1 span {{
            color: #ff6b6b;
            background: rgba(255,107,107,0.15);
            padding: 0 16px;
            border-radius: 12px;
        }}
        .header .tagline {{
            color: rgba(255,255,255,0.7);
            font-size: 1.1rem;
            font-weight: 400;
            margin-top: 6px;
        }}
        .badge-container {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 14px;
        }}
        .badge {{
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(4px);
            padding: 6px 18px;
            border-radius: 40px;
            font-size: 0.75rem;
            font-weight: 600;
            color: rgba(255,255,255,0.85) !important;
            border: 1px solid rgba(255,255,255,0.06);
        }}

        /* ---- GLASS CARDS ---- */
        .card {{
            background: {bg_card};
            {glass}
            padding: 1.5rem 1.8rem;
            border-radius: 20px;
            border: 1px solid {border_color};
            box-shadow: {shadow};
            margin-bottom: 1.2rem;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }}
        .card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 16px 48px rgba(0,0,0,0.12);
            border-color: rgba(255,255,255,0.2);
        }}
        .card h3 {{
            font-size: 1rem;
            font-weight: 700;
            color: {'#1a3a6a' if not dark_mode else '#8ab4f8'} !important;
            margin: 0 0 12px 0;
            padding-bottom: 10px;
            border-bottom: 1px solid {border_color};
            display: flex;
            align-items: center;
            gap: 8px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}
        .card h3 span {{
            font-size: 1.2rem;
        }}

        /* ---- STATS ---- */
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin: 16px 0;
        }}
        .stat-item {{
            background: {stat_bg};
            {glass}
            padding: 1.2rem 1rem;
            border-radius: 16px;
            text-align: center;
            border: 1px solid {border_color};
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        .stat-item::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, #ff6b6b, #ffb347, #48cae4);
        }}
        .stat-item:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        }}
        .stat-item .number {{
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ff6b6b, #ffb347);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.2;
        }}
        .stat-item .label {{
            font-size: 0.7rem;
            color: {text_color};
            opacity: 0.6;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 600;
            margin-top: 4px;
        }}

        /* ---- DONOR CARDS ---- */
        .donor {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: {bg_card};
            {glass}
            border: 1px solid {border_color};
            border-radius: 16px;
            padding: 14px 20px;
            margin: 8px 0;
            transition: all 0.3s ease;
        }}
        .donor:hover {{
            border-color: #ff6b6b;
            box-shadow: 0 8px 24px rgba(255,107,107,0.1);
            transform: translateX(4px);
        }}
        .donor.top {{
            border-color: #ff6b6b;
            background: rgba(255,107,107,0.08);
        }}
        .donor .name-row {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}
        .donor .name {{
            font-weight: 700;
            font-size: 0.95rem;
        }}
        .donor .flag {{
            font-size: 0.6rem;
            font-weight: 700;
            color: #ff6b6b;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}
        .donor .meta {{
            font-size: 0.8rem;
            opacity: 0.7;
        }}
        .donor .dist {{
            font-weight: 700;
            font-size: 1.1rem;
            color: #48cae4;
        }}
        .donor .bg-chip {{
            display: inline-block;
            background: linear-gradient(135deg, #1a3a6a, #2d5a8a);
            color: #fff !important;
            padding: 2px 12px;
            border-radius: 40px;
            font-size: 0.7rem;
            font-weight: 700;
        }}
        .donor .wa {{
            display: inline-block;
            margin-top: 4px;
            font-size: 0.8rem;
            font-weight: 600;
            color: #25D366;
            text-decoration: none;
        }}

        /* ---- BEST MATCH ---- */
        .best-match {{
            background: {bg_card};
            {glass}
            border: 1px solid #ff6b6b;
            border-left: 6px solid #ff6b6b;
            padding: 18px 24px;
            border-radius: 16px;
            margin-top: 16px;
        }}
        .best-match .label {{
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #ff6b6b;
            font-weight: 700;
        }}
        .best-match .phone {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #1a3a6a;
        }}

        /* ---- BUTTONS ---- */
        .stButton > button {{
            background: linear-gradient(135deg, #1a3a6a, #2d5a8a) !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            padding: 0.75rem 1.5rem !important;
            border: none !important;
            border-radius: 40px !important;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            transition: all 0.3s ease !important;
            width: 100% !important;
        }}
        .stButton > button:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 24px rgba(26,58,106,0.3);
            background: linear-gradient(135deg, #2d5a8a, #1a3a6a) !important;
        }}
        .stButton > button:active {{
            transform: scale(0.98);
        }}

        /* ---- SIDEBAR ---- */
        section[data-testid="stSidebar"] {{
            background: {bg_card} !important;
            {glass}
            border-right: 1px solid {border_color};
            padding: 1rem;
        }}
        section[data-testid="stSidebar"] * {{
            color: {text_color} !important;
        }}
        section[data-testid="stSidebar"] h2 {{
            font-size: 0.9rem !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: #1a3a6a !important;
        }}

        /* ---- TABS ---- */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            border-bottom: none;
        }}
        .stTabs [data-baseweb="tab"] {{
            background: transparent !important;
            border-radius: 40px !important;
            padding: 8px 20px !important;
            font-weight: 600 !important;
            color: {text_color} !important;
            opacity: 0.6;
            transition: all 0.3s ease;
            border: 1px solid transparent;
        }}
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, rgba(26,58,106,0.12), rgba(45,90,138,0.12)) !important;
            opacity: 1 !important;
            border-color: rgba(26,58,106,0.2);
            color: #1a3a6a !important;
            font-weight: 700 !important;
        }}

        /* ---- DATA FRAME ---- */
        div[data-testid="stDataFrame"] {{
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid {border_color};
            background: {bg_card} !important;
        }}
        .stDataFrame thead th {{
            background: rgba(26,58,106,0.05) !important;
            font-weight: 700 !important;
            color: {text_color} !important;
            border-bottom: 2px solid {border_color} !important;
        }}
        .stDataFrame tbody td {{
            background: {bg_card} !important;
            color: {text_color} !important;
            border-bottom: 1px solid {border_color} !important;
        }}
        .stDataFrame tbody tr:hover td {{
            background: rgba(26,58,106,0.04) !important;
        }}

        /* ---- MAP ---- */
        .map-box {{
            background: {bg_card};
            {glass}
            border-radius: 20px;
            border: 1px solid {border_color};
            padding: 12px;
            box-shadow: {shadow};
        }}

        /* ---- CONFIRMATION ---- */
        .confirm {{
            background: {bg_card};
            {glass}
            border: 1px solid #1E7B4D;
            border-left: 6px solid #1E7B4D;
            border-radius: 16px;
            padding: 20px 24px;
            margin-top: 14px;
        }}
        .confirm .title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #1E7B4D;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .confirm .row {{
            display: flex;
            gap: 12px;
            font-size: 0.9rem;
            padding: 4px 0;
        }}
        .confirm .row .k {{
            opacity: 0.6;
            min-width: 100px;
        }}
        .confirm .row .v {{
            font-weight: 600;
        }}

        /* ---- FOOTER ---- */
        .footer {{
            text-align: center;
            padding: 1.2rem;
            border-top: 1px solid {border_color};
            margin-top: 2rem;
            opacity: 0.6;
            font-size: 0.85rem;
        }}
        .footer .brand {{
            font-weight: 700;
            color: #1a3a6a;
        }}

        /* ---- RESPONSIVE ---- */
        @media (max-width: 768px) {{
            .stat-grid {{
                grid-template-columns: 1fr 1fr;
            }}
            .header h1 {{
                font-size: 2rem;
            }}
            .card {{
                padding: 1rem;
            }}
        }}
    </style>
    """

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
        <span class="badge">🤖 AI Matching</span>
        <span class="badge">🩸 10,000+ Donors</span>
        <span class="badge">🌍 India-Wide</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# DATA
# ============================================

@st.cache_data
def load_data():
    np.random.seed(42)
    city_coords = {
        'Delhi': (28.6139, 77.2090), 'Mumbai': (19.0760, 72.8777),
        'Chennai': (13.0827, 80.2707), 'Bangalore': (12.9716, 77.5946),
        'Hyderabad': (17.3850, 78.4867), 'Kolkata': (22.5726, 88.3639),
        'Pune': (18.5204, 73.8567), 'Ahmedabad': (23.0225, 72.5714),
        'Jaipur': (26.9124, 75.7873), 'Lucknow': (26.8467, 80.9462)
    }
    blood_groups = ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-']
    first_names = ['Rahul','Priya','Amit','Neha','Vikram','Sneha','Arjun','Meera','Karan','Ananya',
                   'Rohan','Pooja','Suresh','Lakshmi','Manoj','Divya','Naveen','Kavya','Srinivas','Anjali',
                   'Rajesh','Sangeeta','Vijay','Shreya','Ajay','Anita','Sunil','Deepa','Ravi','Sonia']
    last_names = ['Sharma','Patel','Kumar','Singh','Reddy','Gupta','Nair','Iyer','Joshi','Rao',
                  'Verma','Malhotra','Srinivasan','Menon','Shetty','Pillai','Naidu','Das','Ganguly','Bose']

    donors = []
    for i in range(10000):
        city = np.random.choice(list(city_coords.keys()))
        lat, lon = city_coords[city]
        lat += np.random.uniform(-0.5, 0.5)
        lon += np.random.uniform(-0.5, 0.5)
        donors.append({
            'name': f"{np.random.choice(first_names)} {np.random.choice(last_names)}",
            'blood_group': np.random.choice(blood_groups, p=[0.30,0.25,0.20,0.10,0.06,0.04,0.03,0.02]),
            'city': city, 'latitude': lat, 'longitude': lon,
            'phone': f"9{np.random.randint(100000000, 999999999)}",
            'available': np.random.choice(['Yes','Yes','Yes','No'], p=[0.75,0.10,0.10,0.05]),
            'donations': np.random.randint(1, 20)
        })
    return pd.DataFrame(donors)

if 'donors_df' not in st.session_state:
    st.session_state.donors_df = load_data()
df = st.session_state.donors_df

cities = {
    'Delhi': (28.6139, 77.2090), 'Mumbai': (19.0760, 72.8777),
    'Chennai': (13.0827, 80.2707), 'Bangalore': (12.9716, 77.5946),
    'Hyderabad': (17.3850, 78.4867), 'Kolkata': (22.5726, 88.3639),
    'Pune': (18.5204, 73.8567), 'Ahmedabad': (23.0225, 72.5714),
    'Jaipur': (26.9124, 75.7873), 'Lucknow': (26.8467, 80.9462)
}

# ============================================
# COMPATIBILITY & MATCHING
# ============================================

compatibility = {
    'O+': ['O+','O-'], 'O-': ['O-'],
    'A+': ['A+','A-','O+','O-'], 'A-': ['A-','O-'],
    'B+': ['B+','B-','O+','O-'], 'B-': ['B-','O-'],
    'AB+': ['A+','A-','B+','B-','AB+','AB-','O+','O-'],
    'AB-': ['A-','B-','AB-','O-'],
}

def get_compatible(patient_blood):
    return compatibility.get(patient_blood.upper(), [])

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return 2 * R * asin(sqrt(sin((lat2-lat1)/2)**2 + cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2))

def find_donors(patient_lat, patient_lon, patient_blood, urgency='normal'):
    eligible = get_compatible(patient_blood)
    result = df[(df['blood_group'].str.upper().isin(eligible)) & (df['available']=='Yes')].copy()
    if len(result) == 0:
        return None, 0
    result['distance_km'] = result.apply(
        lambda r: haversine(patient_lat, patient_lon, r['latitude'], r['longitude']), axis=1
    )
    urgency_w = {'critical': 0.3, 'urgent': 0.6, 'normal': 1.0}
    result['score'] = result['distance_km'] / 5 * urgency_w.get(urgency.lower(), 1.0)
    result = result.sort_values('score')
    return result.head(5), len(result)

def badge(donations):
    if donations >= 15: return '🏅 Gold'
    if donations >= 10: return '🥈 Silver'
    if donations >= 5: return '🥉 Bronze'
    return '⭐ New'

# ============================================
# NATIONWIDE SUMMARY (GLASS STATS)
# ============================================

total_donors = len(df)
total_available = len(df[df['available'] == 'Yes'])
total_cities = df['city'].nunique()
avg_donations = df['donations'].mean()

st.markdown('<div class="section-label" style="font-size:0.7rem; opacity:0.6; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:0.5rem;">Network — All India</div>', unsafe_allow_html=True)
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown(f'<div class="stat-item"><div class="number">{total_donors:,}</div><div class="label">Total Donors</div></div>', unsafe_allow_html=True)
with s2:
    st.markdown(f'<div class="stat-item"><div class="number">{total_available:,}</div><div class="label">Available Now</div></div>', unsafe_allow_html=True)
with s3:
    st.markdown(f'<div class="stat-item"><div class="number">{total_cities}</div><div class="label">Cities</div></div>', unsafe_allow_html=True)
with s4:
    st.markdown(f'<div class="stat-item"><div class="number">{avg_donations:.1f}</div><div class="label">Avg Donations</div></div>', unsafe_allow_html=True)

st.write("")

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("## 🏆 Top Contributors")
    for _, row in df.nlargest(5, 'donations')[['name','donations']].iterrows():
        st.markdown(f"<div style='display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid rgba(0,0,0,0.05);'><span>{row['name']}</span><span style='font-weight:700; color:#1a3a6a;'>{row['donations']}</span></div>", unsafe_allow_html=True)

    st.markdown("---")
    dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode, key="dark_mode_toggle")
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()

# ============================================
# TABS (now 5)
# ============================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🔍 Find Donors", "📋 Browse Directory", "📝 Register", "🗺️ Map", "🤖 AI Assistant"]
)

# ============================================
# TAB 1: FIND DONORS (unchanged)
# ============================================

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.markdown('<div class="card"><h3>👤 Patient Details</h3>', unsafe_allow_html=True)
            patient_name = st.text_input("Full Name", "Rajesh Kumar", key="patient_name")
            patient_blood = st.selectbox("Blood Group", ['O+','A+','B+','AB+','O-','A-','B-','AB-'], key="patient_blood")
            patient_city = st.selectbox("City", list(cities.keys()), key="patient_city")
            urgency = st.selectbox("Urgency", ['Normal','Urgent','Critical'], key="urgency")
            st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        with st.container():
            st.markdown('<div class="card"><h3>📋 Request Summary</h3>', unsafe_allow_html=True)
            st.markdown(f"**Patient** — {patient_name}")
            st.markdown(f"**Blood group** — {patient_blood}")
            st.markdown(f"**Location** — {patient_city}")
            st.markdown(f"**Urgency** — {urgency}")
            st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍 Find Compatible Donors", key="find_donors_btn"):
        lat, lon = cities.get(patient_city, (28.6139, 77.2090))
        with st.spinner("🤖 Matching against network..."):
            time.sleep(0.6)
            donors, total = find_donors(lat, lon, patient_blood, urgency.lower())

        if donors is None:
            st.error("No compatible donors found in the network.")
        else:
            st.success(f"**{total:,} compatible donors found**, ranked by distance and urgency.")
            if len(donors) < 3:
                st.warning("⚠️ Shortage alert — fewer than 3 compatible donors nearby.", icon="⚠️")

            st.write("")
            for i, (_, donor) in enumerate(donors.iterrows()):
                row_class = "donor top" if i == 0 else "donor"
                wa_link = f"https://wa.me/91{donor['phone']}?text=Hi%20{donor['name'].split()[0]}%2C%20I%20need%20emergency%20blood%20donation."
                flag = '<span class="flag">Best Match</span>' if i == 0 else ''
                st.markdown(f"""
                <div class="{row_class}">
                    <div style="flex:1;">
                        <div class="name-row">
                            <span class="name">{donor['name']}</span> {flag}
                            <span style="font-size:0.7rem; background:rgba(0,0,0,0.05); padding:2px 10px; border-radius:40px;">{badge(donor['donations'])}</span>
                        </div>
                        <div class="meta">{donor['city']} · {donor['phone']}</div>
                        <a class="wa" href="{wa_link}" target="_blank">💬 Contact on WhatsApp →</a>
                    </div>
                    <div style="text-align:right;">
                        <div class="dist">{donor['distance_km']:.1f} km</div>
                        <span class="bg-chip">{donor['blood_group']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            best = donors.iloc[0]
            wa_link = f"https://wa.me/91{best['phone']}?text=Hi%20{best['name'].split()[0]}%2C%20I%20need%20emergency%20blood%20donation."
            st.markdown(f"""
            <div class="best-match">
                <div class="label">🎯 Recommended Contact</div>
                <p style="font-weight:700; font-size:1.05rem; margin:0;">{best['name']} — {best['blood_group']}</p>
                <p class="phone">{best['phone']}</p>
                <p style="margin:2px 0; opacity:0.7;">{best['distance_km']:.1f} km away · approx. {best['distance_km']/30*60:.0f} min</p>
                <a class="wa" href="{wa_link}" target="_blank" style="display:inline-block; margin-top:8px; font-weight:600; color:#25D366; text-decoration:none;">💬 Contact on WhatsApp →</a>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# TAB 2: BROWSE DIRECTORY (unchanged)
# ============================================

with tab2:
    with st.container():
        st.markdown('<div class="card"><h3>🔎 Filter Directory</h3>', unsafe_allow_html=True)
        search_name = st.text_input("Search by Name", placeholder="Type donor name...", key="search_name_dir")
        f1, f2, f3 = st.columns(3)
        with f1:
            filter_bg = st.selectbox("Blood Group", ['All'] + ['O+','A+','B+','AB+','O-','A-','B-','AB-'], key="dir_filter_bg")
        with f2:
            filter_city = st.selectbox("City", ['All'] + list(cities.keys()), key="dir_filter_city")
        with f3:
            filter_avail = st.selectbox("Availability", ['All', 'Available only'], key="dir_filter_avail")
        st.markdown('</div>', unsafe_allow_html=True)

        view = df.copy()
        if filter_bg != 'All':
            view = view[view['blood_group'] == filter_bg]
        if filter_city != 'All':
            view = view[view['city'] == filter_city]
        if filter_avail == 'Available only':
            view = view[view['available'] == 'Yes']
        if search_name:
            view = view[view['name'].str.contains(search_name, case=False)]

        st.markdown(f'<div style="font-size:0.85rem; opacity:0.7; margin-bottom:0.5rem;">{len(view):,} donors match</div>', unsafe_allow_html=True)

        rows_to_show = st.slider("Rows to display", min_value=10, max_value=500, value=100, step=10, key="rows_slider")
        display_df = view[['name', 'blood_group', 'city', 'phone', 'available', 'donations']].rename(columns={
            'name': 'Name', 'blood_group': 'Blood Group', 'city': 'City',
            'phone': 'Phone', 'available': 'Available', 'donations': 'Donations'
        }).head(rows_to_show)
        st.dataframe(display_df, use_container_width=True, height=460, hide_index=True)
        if len(view) > rows_to_show:
            st.caption(f"Showing first {rows_to_show} of {len(view):,} donors.")
        csv = view.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", data=csv, file_name="raktconnect_donors.csv", mime="text/csv", key="download_csv")

# ============================================
# TAB 3: REGISTER (unchanged)
# ============================================

with tab3:
    with st.container():
        st.markdown('<div class="card"><h3>📝 Donor Registration</h3>', unsafe_allow_html=True)
        st.markdown("Join the network to help save lives.")
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Full Name", placeholder="Enter your full name", key="reg_name")
            new_blood = st.selectbox("Blood Group", ['O+','A+','B+','AB+','O-','A-','B-','AB-'], key="reg_blood")
            new_city = st.selectbox("City", list(cities.keys()), key="reg_city")
        with col2:
            new_phone = st.text_input("Phone Number", placeholder="9XXXXXXXXX", key="reg_phone")
            new_available = st.selectbox("Availability", ['Yes','No'], key="reg_available")
            new_donations = st.number_input("Total Past Donations", min_value=0, max_value=50, value=0, key="reg_donations")

        if st.button("✅ Register as Donor", key="register_btn"):
            if not new_name or not new_phone:
                st.error("Please complete all fields.")
            elif len(new_phone) < 10:
                st.error("Please enter a valid 10-digit phone number.")
            else:
                lat, lon = cities.get(new_city, (28.6139, 77.2090))
                lat += np.random.uniform(-0.3, 0.3)
                lon += np.random.uniform(-0.3, 0.3)
                new_donor = pd.DataFrame({
                    'name':[new_name], 'blood_group':[new_blood], 'city':[new_city],
                    'latitude':[lat], 'longitude':[lon], 'phone':[new_phone],
                    'available':[new_available], 'donations':[new_donations]
                })
                st.session_state.donors_df = pd.concat([st.session_state.donors_df, new_donor], ignore_index=True)
                df = st.session_state.donors_df

                donor_id = f"RC-{len(st.session_state.donors_df):06d}"
                st.markdown(f"""
                <div class="confirm">
                    <div class="title"><span style="display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:#1E7B4D; color:#fff; font-weight:800; font-size:1rem;">✓</span> Registration Confirmed</div>
                    <div class="row"><span class="k">Donor ID</span><span class="v">{donor_id}</span></div>
                    <div class="row"><span class="k">Name</span><span class="v">{new_name}</span></div>
                    <div class="row"><span class="k">Blood Group</span><span class="v">{new_blood}</span></div>
                    <div class="row"><span class="k">City</span><span class="v">{new_city}</span></div>
                    <div class="row"><span class="k">Phone</span><span class="v">{new_phone}</span></div>
                    <div class="row"><span class="k">Status</span><span class="v">{"Available" if new_available == "Yes" else "Not available"}</span></div>
                    <p style="margin-top:12px; font-size:0.85rem; opacity:0.7;">Thank you for registering, {new_name.split()[0]}. You may be contacted when a compatible patient nearby needs your blood group.</p>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# TAB 4: MAP (unchanged)
# ============================================

with tab4:
    with st.container():
        st.markdown('<div class="map-box">', unsafe_allow_html=True)
        map_df = df[['latitude','longitude']].dropna()
        if len(map_df) > 0:
            st.map(map_df, zoom=4)
            st.caption(f"📍 {len(map_df)} donor locations across India")
        else:
            st.warning("No donor location data available.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top:1.5rem;"><div style="font-size:0.7rem; opacity:0.6; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:0.5rem;">Donors by City</div></div>', unsafe_allow_html=True)
        st.bar_chart(df['city'].value_counts())

        st.markdown('<div style="margin-top:1.5rem;"><div style="font-size:0.7rem; opacity:0.6; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:0.5rem;">Available Donors by Blood Group</div></div>', unsafe_allow_html=True)
        bg_available = df[df['available'] == 'Yes']['blood_group'].value_counts()
        st.bar_chart(bg_available)

# ============================================
# TAB 5: 🤖 AI ASSISTANT (NEW)
# ============================================

with tab5:
    st.markdown('<div class="card"><h3>🤖 AI Blood Donation Assistant</h3>', unsafe_allow_html=True)
    st.markdown("Ask anything about blood donation, compatibility, emergency procedures, or general health advice.")

    # Check if API key is set
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        ai_available = True
    except (KeyError, AttributeError):
        st.error("❌ Gemini API key not found. Please set `GEMINI_API_KEY` in your Streamlit Cloud secrets.")
        ai_available = False

    # Chat input
    user_question = st.text_input("Your question:", placeholder="e.g., Can O+ donate to AB-?",
                                  key="ai_question", disabled=not ai_available)

    col_ask, col_clear = st.columns([3, 1])
    with col_ask:
        ask_button = st.button("💬 Ask Gemini", use_container_width=True, disabled=not ai_available)
    with col_clear:
        clear_button = st.button("🗑️ Clear History", use_container_width=True, disabled=not ai_available)

    if clear_button:
        st.session_state.ai_chat_history = []
        st.rerun()

    if ask_button and user_question and ai_available:
        # Build a context-aware prompt
        prompt = f"""
        You are RaktConnect's AI blood donation expert. Answer the user's question clearly and helpfully.
        Keep responses concise (2-3 paragraphs) but informative.

        User question: {user_question}

        If the question is about blood compatibility, provide accurate medical information.
        If it's about emergency procedures, guide them to call emergency services immediately.
        If unsure, recommend checking with a medical professional.
        """

        with st.spinner("🧠 Thinking..."):
            try:
                response = model.generate_content(prompt)
                st.session_state.ai_chat_history.append({"user": user_question, "ai": response.text})
            except Exception as e:
                st.error(f"⚠️ AI error: {str(e)}")

    # Display chat history
    if st.session_state.ai_chat_history:
        for entry in st.session_state.ai_chat_history:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 12px 16px; border-radius: 12px; margin: 8px 0; border-left: 4px solid #ff6b6b;">
                <strong style="color: #ff6b6b;">You:</strong> {entry['user']}
            </div>
            <div style="background: rgba(255,255,255,0.02); padding: 12px 16px; border-radius: 12px; margin: 8px 0 16px 0; border-left: 4px solid #48cae4;">
                <strong style="color: #48cae4;">🤖 AI:</strong><br>{entry['ai']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("💡 Your conversation with the AI will appear here. Ask a question above!")

    st.caption("⚠️ For medical emergencies, always call 108 or visit your nearest hospital.")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div class="footer">
    <p><span class="brand">🩸 RaktConnect</span> — Saving lives through intelligent donor matching</p>
    <p style="opacity:0.5; font-size:0.75rem;">Built for CodeStorm 2026: FutureForge</p>
</div>
""", unsafe_allow_html=True)
